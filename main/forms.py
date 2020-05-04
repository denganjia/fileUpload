from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, PasswordField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileRequired, FileAllowed


class LoginForm(FlaskForm):
    account = StringField('账户', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    types = RadioField('选择角色', validators=[DataRequired()], choices=[('student', '学生'), ('teacher', '老师')])
    submit = SubmitField('登录')


class FileUploadForm(FlaskForm):
    upload_set = ['doc', 'docx', 'pdf', 'txt', 'xls', 'jpg', 'png']
    file = FileField('选择文件', validators=[FileRequired(), FileAllowed(upload_set, message="上传的文件不受支持！")])
    submit = SubmitField('提交')


class CreateJobFrom(FlaskForm):
    job_Name = StringField('作业名：', validators=[DataRequired()])
    submit = SubmitField('创建')
