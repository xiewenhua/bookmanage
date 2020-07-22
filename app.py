from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
# import pymysql
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import click
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user
from flask_login import login_required
from flask_login import logout_user
from flask_login import current_user

app = Flask(__name__)
db_uri = "mysql+pymysql://root:root@localhost/books"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'dev'
login_manger = LoginManager(app)
login_manger.login_view='login'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('登出成功！')
    return redirect(url_for('index'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('输入信息不完整,请重新登录！')
            return redirect(url_for('login'))

        user = User.query.first()
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('登录成功！')
            return redirect(url_for('index'))

        flash('密码或用户名不正确，请重新登录！')
        return redirect(url_for('login'))
    return render_template('login.html')


@login_manger.user_loader
def load_user(id):
    user = User.query.get(id)
    return user


@app.cli.command()
@click.option('--username', prompt=True, help='用户名用于登录')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='密码用于登录')
def admin(username, password):
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('更改中...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('创建中...')
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
    db.session.commit()
    click.echo('完成!')


@app.route('/book/edit/<isbn>', methods=["POST", "GET"])
@login_required
def edit(isbn):
    book = Books.query.get_or_404(isbn)
    if request.method == "POST":
        bookname = request.form.get('bookname')
        isbn = request.form.get('isbn')
        score = request.form.get('score')
        if not isbn or not score:
            flash("信息没有填写完整！")
            return redirect(url_for('index'))
        book.bookname = bookname
        book.isbn = isbn
        book.score = score
        db.session.commit()
        flash("修改成功！")
        return redirect(url_for('index'))
    return render_template("edit.html", book=book)


@app.route('/book/delete/<isbn>', methods=["POST"])
@login_required
def delete(isbn):
    book = Books.query.get_or_404(isbn)
    db.session.delete(book)
    db.session.commit()
    flash("删除成功！")
    return redirect(url_for('index'))

@app.route('/settings',methods=['GET','POST'])
@login_required
def settings():
    if request.method=='POST':
        name=request.form['name']

        if not name or len(name)>20:
            flash('请重新输入！')
            return redirect(url_for('settings'))
        
        current_user.name
        db.session.commit()
        flash('名字已更新！')
        return redirect(url_for('index'))
    return render_template('settings.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        bookname = request.form.get('bookname')
        isbn = request.form.get('isbn')
        score = request.form.get('score')
        if not isbn or not score:
            flash("信息没有填写完整！")
            return redirect(url_for('index'))
        book = Books(isbn=isbn, bookname=bookname, score=float(score))
        db.session.add(book)
        try:
            db.session.commit()
        except:
            flash("添加失败，数据库中已存在这个ISBN！")
            return redirect(url_for('index'))
        flash('添加成功！')
        return redirect(url_for('index'))
    q = request.args.get('q')
    if q:
        books = Books.query.filter_by(bookname=q).all()
    else:
        books = Books.query.all()
    return render_template('index.html', books=books)


class Books(db.Model):
    isbn = db.Column(db.String(20), primary_key=True)
    bookname = db.Column(db.String(20))
    score = db.Column(db.Float)


class User(db.Model, UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    # 源码中默认以id作为主键
    # def id(self):
    #     return self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)
