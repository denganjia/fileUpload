from xpinyin import Pinyin
from ext import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

P = Pinyin()


class Student(UserMixin, db.Model):
    """
    学生数据模型
    """
    __tablename__ = 'students'
    s_ID = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    s_Num = db.Column(db.Integer, unique=True)
    s_Name = db.Column(db.String(16), unique=True)
    first_login = db.Column(db.Integer, default=1)
    password_hash = db.Column(db.String(128))

    def __init__(self, Num, Name, first_login):
        self.s_Num = Num
        self.s_Name = Name
        self.first_login = first_login

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Student %r>' % self.name

    def get_id(self):
        return self.s_ID


class Teacher(UserMixin, db.Model):
    """
    教师数据模型
    """
    __tablename__ = 'teachers'
    t_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    t_Account = db.Column(db.String(16), unique=True)
    t_Name = db.Column(db.String(64), unique=True)

    first_login = db.Column(db.Integer, default=1)
    c_Name = db.Column(db.String(), unique=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Teacher %r>' % self.name

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
