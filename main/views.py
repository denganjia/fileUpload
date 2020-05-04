from datetime import datetime
from flask import render_template, redirect, url_for, session
from flask_login import login_user, logout_user, login_required
from models import Teacher, Student

from . import main
from .forms import LoginForm
from .func import Check, Work

from extensions import db, login_manager

login_manager.login_view = 'main.login'


@main.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.types.data == 'student':
            student = Check.stu(form.account.data, form.password.data)
            if student:
                login_user(student)
                return redirect(url_for('main.student_home_page', Account=form.account.data))
        if form.types.data == 'teacher':
            teacher = Check.teacher(form.account.data, form.password.data)
            if teacher:
                login_user(teacher)
                return redirect(url_for('main.teacher_home_page', Account=form.account.data))
    return render_template('Login.html', form=form)


@main.route('/home/student/<Account>', methods=['GET', 'POST'])
@login_required
def student_home_page(Account):
    stu = Student.query.filter_by(s_Num=Account).first()
    job_list = Work.job_need_upload(Account)
    # return 'Hello World!'
    return render_template('studentIndex.html', name=stu.s_Name, list=job_list, schoolNo=Account)


@main.route('/home/teacher/<Account>', methods=['GET', 'POST'])
def teacher_home_page(Account):
    tea = Teacher.query.filter_by(t_Account=Account).first()
    return render_template('teacherIndex.html', name=tea.t_Name)


@login_manager.user_loader
def loader_user(user_id):
    """回调函数，返回用户的登录状态"""
    return Teacher.query.get(int(user_id)) or Student.query.get(int(user_id))
