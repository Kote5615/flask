from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    # about = TextAreaField("Немного о себе")
    submit = SubmitField('Зарегистрироваться')
    sex = SubmitField('Пол')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class SearchForm(FlaskForm):
    name = TextAreaField('Название', validators=[DataRequired()])
    author = TextAreaField('Автор', validators=[DataRequired()])
    submit = SubmitField('Поиск')


class SettingsForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Сохранить изменения')


class BookForm(FlaskForm):
    name = StringField('Название книги', validators=[DataRequired()])
    name_for_search = StringField('Название для поиска', validators=[DataRequired()])
    author = StringField('Автор', validators=[DataRequired()])
    author_for_search = StringField('Автор для поиска', validators=[DataRequired()])
    price = StringField('Цена', validators=[DataRequired()])
    quantity = StringField('Количество', validators=[DataRequired()])
    genre = StringField('Жанр', validators=[DataRequired()])
    category = StringField('Категория', validators=[DataRequired()])
    submit = SubmitField('Добавить книгу в каталог')
