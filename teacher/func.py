from flask import flash

from ext import db
from models import Teacher, Job

from xpinyin import Pinyin as P

import pymysql

conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       password='123456',
                       db='class',
                       charset='utf8')


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
    def creat_job(t_name, classname, job_name, upload_path):
        """
        创建作业
        :param upload_path: 保存上传的作业的路径
        :param classname: 班级名称
        :param t_name: 教师名称
        :param job_name: 作业名称
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
            except():
                conn.rollback()
                db.session.rollback()
                flash("出错！")
            else:
                flash('创建成功')
            finally:
                cursor.close()

    @staticmethod
    def end_job(job_name):
        """
        结束作业
        :param job_name:
        :return:
        """
        cursor = conn.cursor()
        sql = "update jobs set is_over = 1 where job_name = '%s' " % job_name
        cursor.execute(sql)

    @staticmethod
    def delete_job(jobID):
        """
        删除作业
        :param jobID:
        :return:
        """
        cursor = conn.cursor()
        sql_del_jobs = "delete from jobs where job_id = '%s'" % jobID
        sql_del_courses = "alter table courses drop column %s" % jobID
        try:
            cursor.execute(sql_del_jobs)
            cursor.execute(sql_del_courses)

        except():
            flash('删除作业出错')
            conn.rollback()
        else:
            conn.commit()
        finally:
            cursor.close()
