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


@app.route('/search')
def search():
    q = request.args.get('q')
    books = Books.query.filter_by(bookname=q).all()
    return render_template('search.html', books=books)


# @app.context_processor
# def infect_user():
#     books = Books.query.all()
#     return dict(books=books)


@app.route('/book/edit/<isbn>', methods=["POST", "GET"])
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
def delete(isbn):
    book = Books.query.get_or_404(isbn)
    db.session.delete(book)
    db.session.commit()
    flash("删除成功！")
    return redirect(url_for('index'))


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
    q = request.args.get('q')
    if q:
        books = Books.query.filter_by(bookname=q).all()
    else:
        books = Books.query.all()
    return render_template('index.html', books=books)


class Books(db.Model):
    isbn = db.Column(db.String, primary_key=True)
    bookname = db.Column(db.String)
    score = db.Column(db.Float)
