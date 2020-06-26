from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
# import pymysql

app = Flask(__name__)
db_uri = "mysql+pymysql://root:root@localhost/books"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'dev'


@app.context_processor
def infect_user():
    books = Books.query.all()
    return dict(books=books)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
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

    return render_template('index.html')


class Books(db.Model):
    isbn = db.Column(db.String, primary_key=True)
    bookname = db.Column(db.String)
    score = db.Column(db.Float)
