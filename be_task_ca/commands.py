"""
just importing all the models is enough to have them created
"""
# flake8: noqa
from .database import Base, engine
from .item import model as item_model
from .user import model as user_model


def create_db_schema():
    Base.metadata.create_all(bind=engine)
