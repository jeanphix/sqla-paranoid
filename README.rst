Paranoid
========

Brings transparent soft delete to SQLAlchemy ORM.

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

    from .models import (
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


Flask
-----

Paranoid comes with a ready to use ``Flask`` extension built
on top of Flask-SQLAlchemy:


.. code-block:: python

    from paranoid.flask import SQLAlchemy
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker


    db = SQLAlchemy(app)

    Model = db.Model


    class User(Model):
        __softdelete__ = True

        id = Column(Integer, primary_key=True)
        name = Column(String)

    User.query
