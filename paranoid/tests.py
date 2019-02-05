import os

from unittest import TestCase as BaseTestCase

from sqlalchemy import (
    Column,
    create_engine,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import (
    joinedload,
    relationship,
    sessionmaker,
)
from sqlalchemy.orm.exc import NoResultFound

from .models import (
    Model,
    Query,
    Session as ParanoidSession,
    session_factory,
    SqlaSession,
)


metadata = Model.metadata


user_group = Table(
    'user_group',
    metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('group_id', Integer, ForeignKey('group.id'))
)


class Group(Model):
    __tablename__ = 'group'
    __softdelete__ = True

    id = Column(Integer, primary_key=True)
    name = Column(String)


class User(Model):
    __tablename__ = 'user'
    __softdelete__ = True

    id = Column(Integer, primary_key=True)
    name = Column(String)

    groups = relationship(
        Group,
        secondary=user_group,
        backref='users',
    )


engine = create_engine(
    os.environ.get('DATABASE_URL', 'sqlite://'),
    echo=False,
)


class TestCase(BaseTestCase):
    def setUp(self):
        metadata.create_all(engine)
        session = sessionmaker(
            engine,
            class_=ParanoidSession,
            query_cls=Query,
        )()

        admins = Group(name='admins')
        session.add(admins)
        self.admins = admins

        alive = User(name='jeanphix')
        session.add(alive)
        alive.groups.append(admins)
        self.alive = alive

        deleted = User(name='deleted')
        deleted.groups.append(admins)
        session.add(deleted)
        self.deleted = deleted

        session.delete(deleted)
        session.flush()
        session.expire_all()
        self.session = session

    def tearDown(self):
        self.session.rollback()
        metadata.drop_all(engine)


class TestModel(TestCase):
    def test_softdelete(self):
        class SoftDeletable(Model):
            __tablename__ = 'soft'
            __softdelete__ = True

            id = Column(Integer, primary_key=True)

        self.assertIn(
            'deleted_at',
            SoftDeletable.__table__.c,
        )

    def test_harddelete(self):
        class HardDeletable(Model):
            __tablename__ = 'hard'
            __softdelete__ = False

            id = Column(Integer, primary_key=True)

        self.assertNotIn(
            'deleted_at',
            HardDeletable.__table__.c,
        )


class SessionTest(TestCase):
    def test_session_factory(self):
        Session = session_factory(SqlaSession)
        self.assertTrue(issubclass(Session, SqlaSession))

    def test_delete(self):
        alive = self.alive
        self.assertTrue(alive.deleted_at is None)
        session = self.session
        session.delete(alive)
        self.assertTrue(alive.deleted_at is not None)
        session.flush()
        self.assertFalse(alive._sa_instance_state.was_deleted)

    def test_delete_hard(self):
        alive = self.alive
        session = self.session
        session.delete(alive, hard=True)
        session.flush()
        self.assertTrue(alive._sa_instance_state.was_deleted)


class QueryTest(TestCase):
    def test_root(self):
        session = self.session
        query = session.query(User).filter(User.id == self.deleted.id)
        statement = str(query)
        self.assertTrue(statement.endswith(
            'WHERE "user".deleted_at IS NULL AND "user".id = %(id_1)s'
        ))
        self.assertRaises(NoResultFound, query.one)

    def test_joined(self):
        session = self.session
        session.expire_all()
        query = session.query(User).options(
            joinedload(User.groups),
        ).filter(User.id == self.deleted.id)
        statement = str(query)
        self.assertIn(
            'LEFT OUTER JOIN (user_group AS user_group_1 '
            'JOIN "group" AS group_1 ON group_1.id = user_group_1.group_id '
            'AND group_1.deleted_at IS NULL)',
            statement,
        )
        self.assertRaises(NoResultFound, query.one)

    def test_backref(self):
        session = self.session
        session.expire_all()
        query = session.query(Group).options(
            joinedload(Group.users),
        ).filter(Group.id == self.admins.id)
        statement = str(query)
        self.assertIn(
            ' LEFT OUTER JOIN (user_group AS user_group_1 JOIN "user" AS user_1 '
            'ON user_1.id = user_group_1.user_id '
            'AND user_1.deleted_at IS NULL)',
            statement,
        )
        admins = query.one()
        self.assertIn(self.alive, admins.users)
        self.assertNotIn(self.deleted, admins.users)

    def test_lazy_load(self):
        admins = self.admins
        self.assertIn(self.alive, admins.users)
        self.assertNotIn(self.deleted, admins.users)
