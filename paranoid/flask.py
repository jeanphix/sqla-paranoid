from flask_sqlalchemy import (
    Model as BaseModel,
    BaseQuery,
    SignallingSession as BaseSession,
    SQLAlchemy as BaseSQLAlchemy,
)
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
