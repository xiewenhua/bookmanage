from flask import Flask

app=Flask(__name__ )

@app.route('/')
def hello():
    return '欢迎来到我的图书管理系统'