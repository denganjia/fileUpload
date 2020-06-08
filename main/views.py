import os, shutil

from flask import render_template, redirect, url_for, send_from_directory, request, current_app, g, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.utils import secure_filename

# from models import Student, Teacher, Job
from . import main
from .forms import LoginForm, CreateJobFrom, FileUploadForm, ChangePassword
from .func import *
from ext import db, login_manager

login_manager.login_view = 'main.login'
Work = Work()
DateIls = DateIls()


@main.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.types.data == 'student':
            student = check_stu(form.account.data)
            if student:
                if student.first_login == 1:
                    return redirect(url_for('main.chang', account=student.s_Num, role='student', first_login=True))
                elif student.verify_password(form.password.data):
                    login_user(student)
                    return redirect(url_for('main.student_home_page', Account=form.account.data))
                else:
                    flash('账号或密码错误！请重新输入')
            else:
                flash('账号或密码错误！请重新输入')
        if form.types.data == 'teacher':
            teacher = check_teacher(form.account.data)
            if teacher:
                if teacher.first_login == 1:
                    return redirect(url_for('main.chang', account=teacher.t_Account, role='teacher', first_login=True))
                elif teacher.verify_password(form.password.data):
                    login_user(teacher)
                    return redirect(url_for('main.teacher_home_page', Account=form.account.data))
                else:
                    flash('账号或密码错误！请重新输入')
            else:
                flash('账号或密码错误！请重新输入')
    return render_template('login.html', form=form)


@main.route('/changpassword', methods=['GET', 'POST'])
def chang():
    account = request.args.get('account')
    role = request.args.get('role')
    first_login = request.args.get('first_login')
    if request.method == 'GET':
        form = ChangePassword()
        g.form = form
        return render_template('changePassword.html', form=form)
    else:
        if role == 'student':
            student = Student.query.filter_by(s_Num=account).first()
            if first_login:
                student.password = request.form.get('new_password')
                student.first_login = 0
                db.session.add(student)
                db.session.commit()
                return redirect(url_for('main.login'))
            elif student.verify_password(g.form.old_password.data):
                student.password = request.form.get('new_password')
                db.session.add(student)
                db.session.commit()
                return redirect(url_for('main.login'))
            else:
                flash('原密码错误')
        if role == 'teacher':
            teacher = Teacher.query.filter_by(t_Account=account).first()
            if first_login:
                teacher.password = request.form.get('new_password')
                teacher.first_login = 0
                db.session.add(teacher)
                db.session.commit()
                return redirect(url_for('main.login'))
            elif teacher.verify_password(g.form.old_password.data):
                teacher.password = request.form.get('new_password')
                db.session.add(teacher)
                db.session.commit()
                return redirect(url_for('main.login'))
            else:
                flash('原密码错误')


@main.route('/home/student/<Account>', methods=['GET', 'POST'])
@login_required
def student_home_page(Account):
    stu = Student.query.filter_by(s_Num=Account).first()
    job_list = Work.job_need_upload(Account)
    # return 'Hello World!'
    return render_template('stuIndex.html', name=stu.s_Name, list=job_list, schoolNo=Account)


@main.route('/home/teacher/<Account>', methods=['GET', 'POST'])
@login_required
def teacher_home_page(Account):
    tea = Teacher.query.filter_by(t_Account=Account).first()
    form = CreateJobFrom()
    classname = tea.c_Name
    now_job_dict = Work.job_list(tea.t_Name, 0)
    end_job_dict = Work.job_list(tea.t_Name, 1)
    if request.method == 'POST':
        job_name = form.job_Name.data
        upload_path = classname + '\\' + job_name
        try:
            os.makedirs(current_app.config['UPLOAD_FOLDER'] + upload_path)
        except:
            flash("作业已存在")
            return redirect(url_for('main.teacher_home_page', Account=Account))
        Work.creat_job(tea.t_Name, classname, job_name, upload_path)
        return redirect(url_for('main.teacher_home_page', Account=Account))
    return render_template('teachIndex.html', name=tea.t_Name, classname=classname, form=form,
                           job_dict_now=now_job_dict,
                           job_dict_end=end_job_dict)


@main.route('/upload/<schoolNo>/<jobName>', methods=['GET', 'POST'])
@login_required
def file_upload(schoolNo, jobName):
    """
    作业上传
    """
    file_upload_form = FileUploadForm()
    jobs = Job.query.filter_by(job_name=jobName).first()
    if file_upload_form.validate_on_submit():
        file_list = request.files.getlist('file')
        for f in file_list:
            if f and check_file(f.filename):
                filename = secure_filename(f.filename)
                f.save(os.path.join(current_app.config['UPLOAD_FOLDER'] + jobs.job_path, filename))
        Work.sut_change(jobName, schoolNo)
        job_list = Work.job_need_upload(schoolNo)
        return redirect(url_for('main.student_home_page', Account=schoolNo, list=job_list))
    return render_template('upload_file.html', form=file_upload_form)


@main.route('/dateils/<job_id>')
@login_required
def dateils(job_id):
    """返回两个字典：提交和未提交的学号、姓名"""
    job = Job.query.filter_by(job_id=job_id).first()
    is_submit = DateIls.is_submit(job_id)
    no_submit = DateIls.no_submit(job_id)
    return render_template('dateils.html', job_name=job.job_name, isSubmit=is_submit, noSubmit=no_submit)


@main.route('/deljob/<jobID>')
@login_required
def del_job(jobID):
    """删除作业会删除本地存储目录和数据库相关记录"""
    job = Job.query.filter_by(job_id=jobID).first()
    tea = Teacher.query.filter_by(t_Name=job.t_name).first()
    try:
        shutil.rmtree(os.path.join(current_app.config['UPLOAD_FOLDER'], job.job_path))
        Work.delete_job(jobID)
    except:
        return redirect(url_for('main.teacher_home_page', Account=tea.t_Account))
    return redirect(url_for('main.teacher_home_page', Account=tea.t_Account))


@main.route('/endJob/<jobname>')
@login_required
def end_job(jobname):
    """结束作业后，将当前收集的作业打包，数据库作业状态修改为结束"""
    job = Job.query.filter_by(job_name=jobname).first()
    tea = Teacher.query.filter_by(t_Name=job.t_name).first()
    Work.tea_change(jobname)
    base_name = current_app.config['OUTPUT_FOLDER'] + jobname
    for_mat = 'zip'
    root_dir = current_app.config['UPLOAD_FOLDER'] + job.job_path
    shutil.make_archive(base_name, for_mat, root_dir)
    return redirect(url_for('main.teacher_home_page', Account=tea.t_Account))


@main.route('/download/<path:filename>', methods=['GET'])
@login_required
def download(filename):
    """文件下载"""
    dir_path = current_app.config['OUTPUT_FOLDER']
    filename = filename + '.zip'
    return send_from_directory(dir_path, filename, as_attachment=True)


@login_manager.user_loader
def loader_user(user_id):
    """回调函数，返回用户的登录状态"""
    return Teacher.query.get(int(user_id)) or Student.query.get(int(user_id))


@main.route('/logoutUser/', methods=['GET'])
@login_required
def logout():
    """登出用户"""
    logout_user()
    return redirect(url_for('main.login'))
