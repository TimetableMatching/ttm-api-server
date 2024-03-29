from peewee import *
import os
from extension import mydb
import datetime

class BaseModel(Model):
    class Meta:
        database = mydb

class MemberModel(BaseModel):
    id = IntegerField(primary_key=True)
    account = CharField()
    name = CharField()
    password = CharField()
    organization = CharField()

    class Meta:
        db_table = 'member'

class GroupModel(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()

    class Meta:
        db_table = 'groups'

class InvolvedModel(BaseModel):
    is_leader = BooleanField()
    m_id = ForeignKeyField(MemberModel, column_name='m_id')
    g_id = ForeignKeyField(GroupModel, column_name='g_id')

    class Meta:
        db_table = 'involved'

class NoticeModel(BaseModel):
    notice_id = IntegerField(primary_key=True)
    g_id = ForeignKeyField(GroupModel, column_name='g_id')
    text = TextField()
    created_at = DateTimeField(default=datetime.datetime.now())
    author = CharField()

    class Meta:
        db_table = 'notice'

class TableBlankModel(BaseModel):
    m_id = ForeignKeyField(MemberModel, column_name='mem_id')
    day = IntegerField()
    time = IntegerField(primary_key=True)

    class Meta:
        db_table = 'table_blank'
