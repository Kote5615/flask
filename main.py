from flask import Flask, render_template, redirect, request
from data import db_session
from data.users import User
from data.books import Book
from data.user_purchases import Purchase
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from forms.user import RegisterForm, LoginForm, SearchForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

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
            user = User(
                name=form.name.data,
                email=form.email.data,
                hashed_password=form.password.data
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


@app.route("/")
@app.route("/profile")
def profile():
    # form = SearchForm()
    # if form.validate_on_submit():
    #     return redirect('/search/<{}>/<{}>'.format(form.name.data, form.author.data))
    return render_template('profile.html')


@app.route('/add_to_basket/<index>/<author>/<name>', methods=['POST'])
@login_required
def add_to_basket(index, author, name):
    db_sess = db_session.create_session()
    book = db_sess.query(Book).get(index)
    book.quantity = book.quantity - 1
    if book.quantity < 1:
        book.quantity = 0
        book.is_available = 0

    purchase = Purchase(
        user_id=current_user.get_id(),
        book_id=index
    )
    db_sess.add(purchase)
    db_sess.commit()
    return search_results(author, name)


@app.route("/search", methods=['GET', 'POST'])
def search_form():
    form = SearchForm()
    if form.validate_on_submit():
        print(form.name.data, form.author.data)
        # return redirect('/results/<{}>/<{}>'.format(form.author.data, form.name.data))
        return search_results(form.author.data, form.name.data)
    return render_template('search.html', form=form)


@app.route('/results/', methods=['GET', 'POST'])
def search_results(author, name):
    db_sess = db_session.create_session()
    book = db_sess.query(Book).filter((Book.name == name),
    (Book.author == author)).first()
    print(book)
    if not book:
        books = db_sess.query(Book).all()
        return render_template("results.html", title="Ничего не найдено. \n"
                                                     "Ознакомьтесь с нашим каталогом", books=books,
                               author=author, name=name)
    return render_template("result.html", title="Результаты поиска", item=book,
                           author=author, name=name)


def main():
    # bd = input()
    db_session.global_init(f"db/db.db")
    user = User()
    db_sess = db_session.create_session()
    user = db_sess.query(User).first()
    for user in db_sess.query(User).all():
        print(user)

    app.run()


if __name__ == '__main__':
    main()
