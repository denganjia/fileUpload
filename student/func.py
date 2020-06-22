from models import Student, Job
from config import Config
from xpinyin import Pinyin

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


def job_need_upload(schoolNo):
    """

    :param schoolNo:学号
    :return:列表
    """
    cursor = conn.cursor()
    sql = """SELECT COLUMN_NAME from information_schema.columns where TABLE_NAME='courses'"""
    cursor.execute(sql)
    res = cursor.fetchall()
    job_list = []
    # print(res)
    for i in res:
        job_list.append(i[0])
    job_list = job_list[2:]
    # print("job_list", job_list)
    res_list = []
    for j in range(len(job_list)):
        sql = 'select %s from courses where stu_Num = %s'
        cursor.execute(sql, (job_list[j], schoolNo,))
        res = cursor.fetchone()
        # print(res)
        if res[0] == 0:
            res_list.append(job_list[j])
    # print("res_l", res_list)
    job_need_upload_list = []
    for res_l in res_list:
        jobs = Job.query.filter(Job.job_id == res_l).filter(Job.is_over == 0).first()
        try:
            job_need_upload_list.append(jobs.job_name)
        except Exception:
            pass
        # sql = "select job_name from jobs where job_id = %s and is_over = 0;"
        # cursor.execute(sql, (res_l,))
        # res = cursor.fetchone()
        # if res:
        #     job_need_upload_list.append(res[0])

    cursor.close()
    # print("job_need_upload_list", job_need_upload_list)
    return job_need_upload_list
