import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import LoginManager, UserMixin, login_user
from werkzeug.security import check_password_hash, generate_password_hash


class User(SqlAlchemyBase, UserMixin):  # надо обозначить что это класс модели
    __tablename__ = 'users'  # таблица, которая будет создана для хранения данных этой модели
    # jobs = orm.relationship("Jobs", back_populates='user')

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # устанавливает значение хэша пароля для переданной строки
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    # проверяет, правильный ли пароль ввел пользователь
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)