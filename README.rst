Paranoid
========

Brings transparent soft delete to SQLAlchemy ORM. This branch has been
modified to add the with_deleted() and restore() methods for interacting
with soft-deleted resources.

.. image:: https://travis-ci.org/jeanphix/sqla-paranoid.svg?branch=dev
   :target: https://travis-ci.org/jeanphix/sqla-paranoid
   :alt: Build Status


Installation
------------

.. code-block:: bash

    pip install sqla-paranoid


Usage
-----

.. code-block:: python

    from paranoid.models import (
        Model,
        Query,
        Session,
    )

    class User(Model):
        __tablename__ = 'user'
        __softdelete__ = True

        id = Column(Integer, primary_key=True)
        name = Column(String)


    engine = create_engine('sqlite://')
    session = sessionmaker(engine, class_=Session, query_cls=Query)()

    session.query(User)

    # retrieve a user that has not been deleted (assuming ID is 1)
    user = User.query.get(1)

    # soft delete the user
    user.delete()

    # query for a soft deleted user
    user = User.query.with_deleted().get(1)
    # or
    user = User.query.with_deleted().filter_by(id=1)

    # restore the user (undo soft delete)
    user.restore()

    # save the changes
    session.add(user)
    session.commit()

    # hard delete the user
    session.delete(user, hard=True)
    session.commit()


Flask
-----

Paranoid comes with a ready to use ``Flask`` extension built
on top of Flask-SQLAlchemy:


.. code-block:: python

    from paranoid.flask import SQLAlchemy


    db = SQLAlchemy(app)
    # or you can use the factory style of initialisation
    db = SQLAlchemy()
    db.init_app(app)

    Model = db.Model


    class User(Model):
        __softdelete__ = True

        id = Column(Integer, primary_key=True)
        name = Column(String)

    User.query
