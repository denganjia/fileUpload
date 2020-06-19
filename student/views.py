import os

from flask import render_template, redirect, url_for, request, current_app, session
from flask_login import login_user, logout_user, login_required
from werkzeug.utils import secure_filename

from . import students
from .forms import LoginForm, FileUploadForm, ChangePasswordForm
from .func import *
from ext import db, login_manager

login_manager.login_view = 'students.login'


@students.route('/students/', methods=['GET', 'POST'])
def login():
    """
    登录视图
    :return:
    """
    form = LoginForm()
    if request.method == 'POST':
        student_check = StudentFuc.check_stu(form.account.data)
        if student_check:
            if student_check.verify_password(form.password.data):
                session['stu_name'] = student_check.s_Name
                session['schoolNumber'] = student_check.s_Num
                login_user(student_check)
                return redirect(url_for('students.home_page', account=student_check.s_Num))
            elif student_check.first_login == 1:
                return redirect(url_for('students.change_password', account=student_check.s_Num, first_login=1))
            else:
                flash("账号或密码错误！请重新输入")
        else:
            flash("账号或密码错误！请重新输入")
    return render_template('login.html', form=form)


@students.route('/students/change_password<account>', methods=['GET', 'POST'])
def change_password(account):
    first_login = request.args.get('first_login')  # 获取账户是不是第一次登录
    form = ChangePasswordForm()
    if request.method == 'POST':
        student = Student.query.filter_by(s_Num=account).first()
        if first_login:
            student.password = request.form.get('new_password')
            student.first_login = 0
            db.session.add(student)
            db.session.commit()
            return redirect(url_for('students.login'))
        elif student.verify_password(form.old_password.data):
            student.password = request.form.get('new_password')
            db.session.add(student)
            db.session.commit()
            return redirect(url_for('students.login'))
    else:
        return render_template('changePassword.html', form=form)


@students.route('/students/home_page/<account>', methods=['GET', 'POST'])
@login_required
def home_page(account):
    stu_name = session.get('stu_name')
    job_list = StudentFuc.job_need_upload(account)
    return render_template('stuIndex.html', name=stu_name, list=job_list, schoolNum=account)


@students.route('/students/upload<jobName>', methods=['GET', 'POST'])
@login_required
def file_upload(jobName):
    school_number = session.get('schoolNumber')
    upload_form = FileUploadForm()
    jobs = Job.query.filter_by(job_name=jobName).first()
    if request.method == 'POST':
        file_list = request.files.getlist('file')
        for file in file_list:
            if file and StudentFuc.check_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'] + jobs.job_path, filename))
        StudentFuc.stu_change(jobName, school_number)
        job_list = StudentFuc.job_need_upload(school_number)
        return redirect(url_for('student.home_page', account=school_number, list=job_list))
    return render_template('upload_file.html', form=upload_form)


@login_manager.user_loader
def loader_user(user_id):
    return Student.query.get(int(user_id))


@students.route('/students/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('students.login'))
