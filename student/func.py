from models import Student, Job
from config import Config
from xpinyin import Pinyin
from flask import flash

import pymysql

P = Pinyin()
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       password='123456',
                       db='class',
                       charset='utf8')


class StudentFuc:

    @staticmethod
    def check_stu(Account):
        """

        :param Account: 学号
        :return: 返回SQL alchemy对象
        """
        stu = Student.query.filter_by(s_Num=Account).first()
        return stu

    @staticmethod
    def stu_change(jobName, schoolNo):
        """
        如果作业提交，就在数据库中将此作业修改为1
        :param jobName:作业名称/任务名称
        :param schoolNo:学号
        :return:
        """
        jobs = Job.query.filter_by(job_name=jobName).first()
        cursor = conn.cursor()
        sql = 'update courses set %s = 1 where stu_Num = %s ' % (jobs.job_id, schoolNo)
        cursor.execute(sql)
        conn.commit()
        cursor.close()

    @staticmethod
    def check_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

    @staticmethod
    def job_need_upload(schoolNo):
        """

        :param schoolNo:学号
        :return:返回学生没有提交的作业
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
        for i in res_l:
            jobs = Job.query.filter_by(job_id=str(i), is_over=0)  # "select job_name from jobs where job_id = '%s'" % i
            # cursor.execute(sql)
            # res = cursor.fetchall()
            for job in jobs:
                job_need_upload_list.append(job.job_name)
        cursor.close()
        return job_need_upload_list

    @staticmethod
    def job_list(t_name, n):
        """
        :param t_name: 课程名
        :param n: 1 or 0
        :return: 返回作业列表
        """
        jobs = Job.query.filter_by(t_name=t_name, is_over=n).all()
        jobs_name_dict = {}
        for job in jobs:
            jobs_name_dict[job.job_name] = job.job_id
        return jobs_name_dict

    @staticmethod
    def delete_job(jobID):
        """

        :param jobID: 课程ID
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
