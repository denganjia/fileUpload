import os

import random
import string
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	SECRET_KEY = ''.join(random.sample(string.ascii_letters + string.digits, 8))
	SQLALCHEMY_COMMIT_ON_TEARDOWN = False
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)
	UPLOAD_FOLDER = os.getcwd() + '\\upload\\'
	OUTPUT_FOLDER = os.getcwd() + '\\download\\'
	ALLOWED_EXTENSIONS = {'doc', 'docx', 'txt', 'jpg', 'png', 'zip', 'rar', 'pkt', 'pka'}

	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
	                          'mysql+pymysql://root:root@192.168.25.128/class'


config = {
	'development': DevelopmentConfig,
	'default': DevelopmentConfig
}
