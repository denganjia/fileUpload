# _*_coding : utf-8 _*_
# @Time     : 2020/4/8 14:58
# @Author   : 池鱼
# @Filename : forms.py

from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, FileField, StringField, RadioField, MultipleFileField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_wtf.file import FileAllowed, FileRequired


class LoginForm(FlaskForm):
    account = StringField(render_kw={'placeholder': '账号'}, validators=[DataRequired(message=u'账户不能为空')])
    password = PasswordField(render_kw={'placeholder': '密码'}, validators=[DataRequired(message=u'密码不能为空')])
    types = RadioField(validators=[DataRequired()], choices=[('student', '学生'), ('teacher', '老师')])
    submit = SubmitField('登录')


class FileUploadForm(FlaskForm):
    upload_set = ['doc', 'docx', 'pdf', 'txt', 'xls', 'jpg', 'png']
    file = MultipleFileField('选择文件', validators=[MultipleFileField(), FileAllowed(upload_set, message="上传的文件不受支持！")])
    submit = SubmitField('提交')


class CreateJobFrom(FlaskForm):
    job_Name = StringField('作业名：', validators=[DataRequired()])
    submit = SubmitField('创建')


class ChangePassword(FlaskForm):
    old_password = PasswordField('旧密码', render_kw={'placeholder': '旧密码'}, validators=[DataRequired()])
    new_password = PasswordField('新密码', render_kw={'placeholder': '新密码'}, validators=[DataRequired(), Length(min=6)])
    new_password_repeat = PasswordField('确认新密码', render_kw={'placeholder': '确认新密码'},
                                        validators=[DataRequired(), EqualTo(new_password)])
    submit = SubmitField('提交')
