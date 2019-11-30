from peewee import *
import os
from extension import mydb

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
    m_id = ForeignKeyField(MemberModel, column_name='id')
    g_id = ForeignKeyField(GroupModel, column_name='id')

    class Meta:
        db_table = 'involved'

class NoticeModel(BaseModel):
    notice_id = IntegerField(primary_key=True)
    g_id = ForeignKeyField(GroupModel, column_name='id')
    text = TextField()

    class Meta:
        db_table = 'notice'

class TableBlankModel(BaseModel):
    m_id = ForeignKeyField(MemberModel, column_name='m_id')
    day = IntegerField()
    time = IntegerField(primary_key=True)

    class Meta:
        db_table = 'table_blank'
