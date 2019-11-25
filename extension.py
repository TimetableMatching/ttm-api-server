from peewee import *
import ssl
from playhouse.db_url import connect
import pymysql
from config import DB_URL

SQL_DB_URL = DB_URL

mydb=connect(SQL_DB_URL)