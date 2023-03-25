import sqlalchemy
from data.db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Books(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String,
                             nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer,
                              nullable=True)
    is_available = sqlalchemy.Column(sqlalchemy.Boolean,
                                     nullable=True)
