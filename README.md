# bookmanage
基于Flask框架的简单图书管理系统

## 不完全运行步骤

1. 安装&运行虚拟环境
```
pipenv install
pipenv shell
```
2. 创建数据库，导入数据
``` sql
CREATE DATABASE books;
SOURCE <create.sql>;
SOURCE <data.sql>;
```
2. 运行项目
```
flask run -p 12555 --host=0.0.0.0
```
