# _*_coding : utf-8 _*_
# @Time     : 2020/4/8 17:24
# @Author   : 池鱼
# @Filename : ext.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import pymysql

conn = pymysql.connect(host='192.168.25.128',
                       port=3306,
                       user='root',
                       password='root',
                       db='class',
                       charset='utf8')
db = SQLAlchemy()
login_manager = LoginManager()