from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
# import pymysql

app = Flask(__name__)
db_uri = "mysql+pymysql://root:root@localhost/books"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

@app.context_processor
def infect_user():
    books=Books.query.all()
    return dict(books=books)

@app.route('/')
def index():
    return render_template('index.html')


class Books(db.Model):
    isbn=db.Column(db.String,primary_key=True)
    bookname=db.Column(db.String)
    score=db.Column(db.Float)
