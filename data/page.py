import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from flask_login import UserMixin


class Advertisement(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'advertisement'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    enabled = sqlalchemy.Column(sqlalchemy.BOOLEAN, nullable=True)
