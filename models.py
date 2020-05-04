from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql

from extensions import db

conn = pymysql.connect(host='192.168.25.128',
                       port=3306,
                       user='root',
                       password='root',
                       db='class',
                       charset='utf8')


class Student(db.Model, UserMixin):
    __tablename__ = 'students'
    s_ID = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    s_Num = db.Column(db.Integer, unique=True)
    s_Name = db.Column(db.String(16), unique=True)
    s_Password = db.Column(db.String(16))
    password_hash = db.Column(db.String(128))

    def get_id(self):
        return self.s_ID


class Teacher(db.Model, UserMixin):
    __tablename__ = 'teachers'
    t_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    t_Account = db.Column(db.String(16), unique=True)
    t_Name = db.Column(db.String(64), unique=True)
    t_Password = db.Column(db.String(64))
    c_Name = db.Column(db.String(), unique=True)
    password_hash = db.Column(db.String(128))

    def get_id(self):
        return self.t_ID


class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_name = db.Column(db.String(64), unique=True)
    t_name = db.Column(db.String(16), unique=True)
    job_id = db.Column(db.String(64), unique=True)
    is_over = db.Column(db.Integer, default=0)
    job_path = db.Column(db.String(16))
