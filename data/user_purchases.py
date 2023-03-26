import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class Purchase(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'user_purchases'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    book_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
