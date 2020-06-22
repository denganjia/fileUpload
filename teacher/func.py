from flask import flash, redirect

from ext import db
from models import Teacher, Job

from xpinyin import Pinyin

import pymysql

conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       password='123456',
                       db='class',
                       charset='utf8')

P = Pinyin()


def check_teacher(Account):
    teacher = Teacher.query.filter_by(t_Account=Account).first()
    return teacher


class TeachersFuc:
    @staticmethod
    def job_list(t_name, n):
        jobs = Job.query.filter_by(t_name=t_name, is_over=n).all()
        jobs_name_dict = {}
        for job in jobs:
            jobs_name_dict[job.job_name] = job.job_id
        return jobs_name_dict

    @staticmethod
    def no_submit(job_id):
        cursor = conn.cursor()
        sql = "select stu_Num,stu_Name from courses where %s = 0 " % job_id
        try:
            cursor.execute(sql)
            res_list = cursor.fetchall()
            no_submit_dict = {}
            for res in res_list:
                no_submit_dict[res[0]] = res[1]
            return no_submit_dict
        except():
            raise AttributeError('出错了')
        finally:
            cursor.close()

    @staticmethod
    def is_submit(job_id):
        cursor = conn.cursor()
        sql = "select stu_Num,stu_Name from courses where %s = 1" % job_id
        try:
            cursor.execute(sql)
            res_list = cursor.fetchall()
            is_submit_dict = {}
            for res in res_list:
                is_submit_dict[res[0]] = res[1]
            return is_submit_dict
        except():
            flash('出错了')
        finally:
            cursor.close()

    @staticmethod
    def creat_job(t_name, classname, jobName, upload_path):
        """
        创建作业
        :param upload_path: 保存上传的作业的路径
        :param classname: 班级名称
        :param t_name: 教师名称
        :param jobName: 作业名称
        :return:
        """
        cursor = conn.cursor()
        jobs = Job.query.filter_by(job_name=classname + jobName).first()
        if jobs:
            flash('作业已存在')
        else:
            _job_id = P.get_initials(classname + jobName, '')
            job_creat = Job(job_name=classname + jobName, t_name=t_name, job_id=_job_id, job_path=upload_path)
            # sql = "insert into jobs(jobs,is_over,job_id) values ('%s',0,'%s')" % (classname + job_name, job_id)
            sql = "alter table `courses` add {} int default 0;"
            try:
                cursor.execute(sql.format(_job_id))
                db.session.add(job_creat)

            except():
                conn.rollback()
                db.session.rollback()
            else:
                db.session.commit()
                flash('创建成功')

    @staticmethod
    def end_job(job_name):
        """
        结束作业
        :param job_name:
        :return:
        """
        cursor = conn.cursor()
        sql = "update jobs set is_over = 1 where job_name = %s "
        try:
            cursor.execute(sql, (job_name,))
        except (Exception):
            flash('出错了！')
            cursor.close()

    @staticmethod
    def delete_job(jobID):
        """
        删除作业
        :param jobID:
        :return:
        """
        cursor = conn.cursor()
        sql_del_jobs = "delete from jobs where job_id = %s"
        sql_del_courses = "alter table courses drop column {}"
        try:
            cursor.execute(sql_del_jobs, (jobID,))
            cursor.execute(sql_del_courses.format(jobID))
        except():
            flash('删除作业出错')
            conn.rollback()
        else:
            conn.commit()
        finally:
            cursor.close()
            return 0
