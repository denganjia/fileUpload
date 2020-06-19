import os
import shutil

from flask import render_template, redirect, url_for, request, current_app, session, send_from_directory
from flask_login import login_user, logout_user, login_required

from . import teachers
from .forms import LoginForm, ChangePasswordForm, CreateJobFrom
from .func import *
from ext import db, login_manager

login_manager.login_view = 'teachers.login'


@teachers.route('/teachers/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        teacher = check_teacher(form.account.data)
        if teacher:
            if teacher.verify_password(form.password.data):
                login_user(teacher)
                session['teacher_name'] = teacher.t_Name
                # session['teacher_account'] = teacher.t_Account
                session['class_name'] = teacher.c_Name
                return redirect(url_for('teachers.home_page', account=teacher.t_Account))
            elif teacher.first_login == 1:
                return redirect(url_for('teachers.change_password', account=teacher.t_Account, first_login=1))
            else:
                flash("账号或密码错误！请重新输入")
        else:
            flash("账号或密码错误！请重新输入")
    return render_template('login.html', form=form)


@teachers.route('/teachers/home_page?<account>', methods=['GET', 'POST'])
@login_required
def home_page(account):
    form = CreateJobFrom()
    teacher_name = session.get('teacher_name')
    # teacher_account = session.get('teacher_account')
    t_account = account
    class_name = session.get('class_name')
    now_job_dic = TeachersFuc.job_list(teacher_name, 0)
    end_job_dic = TeachersFuc.job_list(teacher_name, 1)
    if form.validate_on_submit():
        new_job_name = form.job_Name.data
        upload_path = class_name + '/' + new_job_name
        try:
            os.mkdir(current_app.config['UPLOAD_FOLDER'] + upload_path)
        except():
            flash("作业已存在!")
        TeachersFuc.creat_job(teacher_name, class_name, new_job_name, upload_path)
        return redirect(url_for('teachers.home_page', account=t_account))
    return render_template('teachIndex.html', name=teacher_name, class_name=class_name,
                           form=form, job_dict_now=now_job_dic,
                           job_dict_end=end_job_dic)


@teachers.route('/teachers/change_password<account>', methods=['GET', 'POST'])
def change_password(account):
    teacher = Teacher.query.filter_by(t_Account=account).first()
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if request.args.get('first_login'):
            teacher.password = request.form.get('new_password')
            teacher.first_login = 0
            db.session.add(teacher)
            db.session.commit()
            return redirect(url_for('main.login'))
        elif teacher.verify_password(form.old_password.data):
            teacher.password = request.form.get('new_password')
            db.session.add(teacher)
            db.session.commit()
            return redirect(url_for('main.login'))
        else:
            flash('原密码错误')
    else:
        return render_template('changePassword.html', form=form)


@teachers.route('/download/<path:filename>', methods=['GET'])
@login_required
def download(filename):
    """文件下载"""
    dir_path = current_app.config['OUTPUT_FOLDER']
    filename = filename + '.zip'
    return send_from_directory(dir_path, filename, as_attachment=True)


@teachers.route('/endJob/<job_name>')
@login_required
def end_job(job_name):
    """结束作业后，将当前收集的作业打包，数据库作业状态修改为结束"""
    job = Job.query.filter_by(job_name=job_name).first()
    tea = Teacher.query.filter_by(t_Name=job.t_name).first()
    TeachersFuc.end_job(job_name)
    base_name = current_app.config['OUTPUT_FOLDER'] + job_name
    for_mat = 'zip'
    root_dir = current_app.config['UPLOAD_FOLDER'] + job.job_path
    shutil.make_archive(base_name, for_mat, root_dir)
    return redirect(url_for('main.teacher_home_page', Account=tea.t_Account))


@teachers.route('/delete_job/<jobID>')
@login_required
def del_job(jobID):
    """删除作业会删除本地存储目录和数据库相关记录"""
    job = Job.query.filter_by(job_id=jobID).first()
    tea = Teacher.query.filter_by(t_Name=job.t_name).first()
    try:
        shutil.rmtree(os.path.join(current_app.config['UPLOAD_FOLDER'], job.job_path))
        TeachersFuc.delete_job(jobID)
    except():
        return redirect(url_for('main.teacher_home_page', Account=tea.t_Account))
    return redirect(url_for('main.teacher_home_page', Account=tea.t_Account))


@teachers.route('/details/<job_id>')
@login_required
def details(job_id):
    """返回两个字典：提交和未提交的学号、姓名"""
    job = Job.query.filter_by(job_id=job_id).first()
    is_submit = TeachersFuc.is_submit(job_id)
    no_submit = TeachersFuc.no_submit(job_id)
    return render_template('details.html', job_name=job.job_name, isSubmit=is_submit, noSubmit=no_submit)


@login_manager.user_loader
def user_loader(user_id):
    return Teacher.query.get(int(user_id))


@teachers.route('/teachers/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.main'))
