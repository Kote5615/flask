import os

from flask import Flask, render_template, redirect, request
from data import db_session
from data.users import User
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from data.db_session import SqlAlchemyBase
import calendar
from werkzeug.utils import secure_filename
from forms.user import RegisterForm, LoginForm, SettingsForm

UPLOAD_FOLDER = 'static/icons/'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
    else:
        form = RegisterForm()

        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть")
            sex = request.form['sex']
            if sex == 'female':
                icon = 'free-icon-single-person-5231019.png'
            else:
                icon = 'free-icon-young-man-4440953.png'
            user = User(
                name=form.name.data,
                email=form.email.data,
                hashed_password=form.password.data,
                sex=sex,
                icon=icon
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')
        return render_template('register.html', title='Registration', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    else:
        form = LoginForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")

            return render_template('login.html',
                                   message="Неправильный логин или пароль",
                                   form=form)
        return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def iconoutput():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        icon = db_sess.query(User.icon).filter(User.id == current_user.get_id()).first()
        print(icon)
        return str(icon)[2:-3]


@app.route("/")
@app.route("/profile")
def profile():
    if current_user.is_authenticated:
        db_sess = db_session.create_session()
        reg_date = db_sess.query(User.reg_date).filter(User.id == current_user.get_id()).first()
        sub = db_sess.query(User.subscribe).filter(User.id == current_user.get_id()).first()
        name = db_sess.query(User.name).filter(User.id == current_user.get_id()).first()

        about = db_sess.query(User.about).filter(User.id == current_user.get_id()).first()
        # print(about)
        # print(name)
        name = str(name)[2:-3].capitalize()
        if str(about)[1:-2].capitalize() == 'None':
            about = str(about)[1:-2].capitalize()
        else:
            about = str(about)[2:-3].capitalize()
        # print(about)
        if str(sub) == '(True,)':
            sub = 'оформлена'
        else:
            sub = 'не оформлена'
        reg_date = str(reg_date)[19:30].split(',')
        # print(iconoutput())
        reg_year = reg_date[0]
        reg_month = reg_date[1]
        reg_month = calendar.month_name[int(reg_month)]
        red_day = reg_date[2]
        reg_date = f'{red_day} {reg_month} {reg_year}'
        return render_template('profile.html', reg_date=reg_date, sub=sub, icon=iconoutput(), name=name, about=about)
    else:
        return redirect("/login")


@app.route("/settings", methods=['POST', 'GET'])
@app.route("/modify", methods=['POST', 'GET'])
def settings():
    if current_user.is_authenticated:
        form = SettingsForm()

        db_sess = db_session.create_session()
        email = db_sess.query(User.email).filter(User.id == current_user.get_id()).first()
        user = current_user

        print(user.id)

        if request.method == 'POST':
            f = request.files['file']
            print(request.form['about'], 'about')
            if request.form['about'].replace("", "") == '':
                about = None
            else:
                about = request.form['about']
            if str(f) == "<FileStorage: '' ('application/octet-stream')>":
                if user.sex == 'female':
                    filename = 'free-icon-single-person-5231019.png'
                else:
                    filename = 'free-icon-young-man-4440953.png'
                num_rows_updated = db_sess.query(User).filter(User.id == current_user.get_id()).update(
                    dict(icon=filename, about=about))
                db_sess.commit()
            else:
                filename = f'{str(email)[2:-3]}.jpg'
                f.save(app.config['UPLOAD_FOLDER'] + filename)
                num_rows_updated = db_sess.query(User).filter(User.id == current_user.get_id()).update(
                    dict(icon=filename, about=about))

                db_sess.commit()
            return redirect("/profile")
        return render_template('settings.html')

    else:
        return redirect("/login")


def main():
    # bd = input()
    db_session.global_init(f"db/db.db")
    user = User()
    db_sess = db_session.create_session()
    user = db_sess.query(User).first()
    # for user in db_sess.query(User).all():
    #     print(user)

    app.run()


if __name__ == '__main__':
    main()
