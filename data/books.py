import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class Book(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    quantity = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    is_available = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
