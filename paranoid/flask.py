from flask_sqlalchemy import SQLAlchemy as BaseSQLAlchemy
from flask_sqlalchemy.model import Model as BaseModel
from flask_sqlalchemy.query import Query as BaseQuery
from flask_sqlalchemy.session import Session as BaseSession

from sqlalchemy import orm

from .models import (
    model_factory,
    query_factory,
    session_factory,
)


Query = query_factory(BaseQuery)

Model = model_factory(BaseModel)
Model.query_class = Query

Session = session_factory(BaseSession)


class SQLAlchemy(BaseSQLAlchemy):
    def __init__(self, *args, model_class=Model, **kwargs):
        super().__init__(*args, model_class=model_class, **kwargs)

    def create_session(self, options):
        return orm.sessionmaker(class_=Session, db=self, **options)
