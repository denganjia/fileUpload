from flask import flash

from ext import db
from models import Student, Teacher, Job
from app import config_name
from xpinyin import Pinyin
from config import Config

import pymysql

P = Pinyin()
if config_name == 'default' or 'development':
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='123456',
                           db='class',
                           charset='utf8')
elif config_name == 'production':
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='root',
                           db='class',
                           charset='utf8')


def check_stu(Account):
    stu = Student.query.filter_by(s_Num=Account).first()
    return stu


def check_teacher(Account):
    teacher = Teacher.query.filter_by(t_Account=Account).first()
    return teacher


def check_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


class DateIls:
    """
    返回两个字典，一个是交了作业，一个是没交
    """

    def no_submit(self, job_id):
        cursor = conn.cursor()
        sql = "select stu_Num,stu_Name from courses where %s = 0 " % job_id
        try:
            cursor.execute(sql)
            res_list = cursor.fetchall()
            no_submit_dict = {}
            for res in res_list:
                no_submit_dict[res[0]] = res[1]
            return no_submit_dict
        except:
            raise AttributeError('出错了')
        finally:
            cursor.close()

    def is_submit(self, job_id):
        cursor = conn.cursor()
        sql = "select stu_Num,stu_Name from courses where %s = 1" % job_id
        try:
            cursor.execute(sql)
            res_list = cursor.fetchall()
            is_submit_dict = {}
            for res in res_list:
                is_submit_dict[res[0]] = res[1]
            return is_submit_dict
        except:
            flash('出错了')
        finally:
            cursor.close()


class Work:
    def creat_job(self, t_name, classname, job_name, upload_path):
        """
        创建作业
        :param job_name:
        :return:
        """
        cursor = conn.cursor()
        jobs = Job.query.filter_by(job_name=classname + job_name).first()
        if jobs:
            flash('作业已存在')
        else:
            job_id = P.get_initials(classname, '') + P.get_initials(job_name, '')
            job_creat = Job(job_name=classname + job_name, t_name=t_name, job_id=job_id, job_path=upload_path)
            # sql = "insert into jobs(jobs,is_over,job_id) values ('%s',0,'%s')" % (classname + job_name, job_id)
            sql_courses_alter = 'alter table courses add %s int default 0 ' % job_id
            try:
                db.session.add(job_creat)
                cursor.execute(sql_courses_alter)
                db.session.commit()
            except:
                conn.rollback()
                db.session.rollback()
                flash("出错！")
            else:
                flash('创建成功')
            finally:
                cursor.close()

    def sut_change(slef, jobName, schoolNo):
        """
        如果作业提交，就在数据库中将此作业修改为1
        :param jobName:
        :param schoolNo:
        :return:
        """
        jobs = Job.query.filter_by(job_name=jobName).first()
        cursor = conn.cursor()
        sql = 'update courses set %s = 1 where stu_Num = %s ' % (jobs.job_id, schoolNo)
        cursor.execute(sql)
        conn.commit()
        cursor.close()

    def tea_change(self, jobname):
        cursor = conn.cursor()
        sql = "update jobs set is_over = 1 where job_name = '%s' " % jobname
        cursor.execute(sql)

    def job_need_upload(self, schoolNo):
        """
        返回学生没有提交的作业
        :param schoolNo:
        :return:
        """
        cursor = conn.cursor()
        sql = """SELECT COLUMN_NAME from information_schema.columns where TABLE_NAME='courses'"""
        cursor.execute(sql)
        res = cursor.fetchall()
        job_list = []
        for i in res:
            job_list.append(i[0])
        job_list = job_list[2:]
        res_l = []
        for j in range(len(job_list)):
            sql = 'select %s from courses where stu_Num = %s' % (job_list[j], schoolNo)
            cursor.execute(sql)
            res = cursor.fetchone()
            if res[0] == 0:
                res_l.append(job_list[j])
        job_need_upload_list = []
        for i in (res_l):
            jobs = Job.query.filter_by(job_id=str(i), is_over=0)  # "select job_name from jobs where job_id = '%s'" % i
            # cursor.execute(sql)
            # res = cursor.fetchall()
            for job in jobs:
                job_need_upload_list.append(job.job_name)
        cursor.close()
        return job_need_upload_list

    def job_list(self, t_name, n):
        jobs = Job.query.filter_by(t_name=t_name, is_over=n).all()
        jobs_name_dict = {}
        for job in jobs:
            jobs_name_dict[job.job_name] = job.job_id
        return jobs_name_dict

    def delete_job(self, jobID):
        cursor = conn.cursor()
        sql_del_jobs = "delete from jobs where job_id = '%s'" % jobID
        sql_del_courses = "alter table courses drop column %s" % jobID
        try:
            cursor.execute(sql_del_jobs)
            cursor.execute(sql_del_courses)
        except:
            flash('删除作业出错')
            conn.rollback()
        else:
            cursor.commit()
        finally:
            cursor.close()
