from flask_restful import Resource, Api
from flask_restful import reqparse
from extension import mydb
from model import *

import hashlib

db = mydb

class CreateUser(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str)
            parser.add_argument('password', type=str)
            parser.add_argument('name', type=str)
            parser.add_argument('organization', type=str)
            parser.add_argument('schedule', action='append')
            args = parser.parse_args()
            
            ret = {
                'result_message': '',
                'status':str(0),
            }
            with db.atomic() as transaction:
                try:
                    encoded_pw = hashlib\
                        .sha256( str(args['password']).encode()).hexdigest()

                    MemberModel.create(
                        account=str(args['email']),
                        name = str(args['name']),
                        password = encoded_pw,
                        organization = str(args['organization']),
                    )


                except Exception as e:
                    transaction.rollback()
                    ret['result_message']='DB'+str(e)
                    return ret

            # debug test
            #args['schedule'] = ["12","21","23","32"]
            with db.atomic() as transaction:
                try:
                    query = MemberModel\
                    .select(MemberModel.id)\
                    .where(MemberModel.account == args['email'])
                    ok = False
                    m_id = 0
                    for ac in query:
                        m_id = ac.id

                    for sc in args['schedule']:
                        TableBlankModel.create(
                            m_id = m_id,
                            day = int(sc[0]),
                            time = int(sc[1]),
                        )

                except Exception as e:
                    transaction.rollback()
                    ret['result_message']='DB'+str(e)
                    return ret

            ret['status']=str(1)
            ret['email']=args['email']
            ret['result_message']='success'

            return ret

        except Exception as e:
            return {'error': str(e), 'status':str(0)}


class DeleteUser(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str)
            parser.add_argument('password', type=str)
            args = parser.parse_args()

            with db.atomic() as transaction:
                try :                    
                    nrows = MemberModel.delete()\
                            .where(MemberModel.account == args['email'])\
                            .execute()

                    if nrows == 0:
                        raise Exception('Can`t Delete Account '+args['email'])

                except Exception as e:
                    transaction.rollback()
                    return{
                        'result_message': 'DB:'+str(e),
                        'status' : str(0)
                    }

            return {
                'status': str(1),
                'result_message': 'succeed to delete user '+args['email'],
            }
        except Exception as e:
            return {
                'error': str(e),
                'status': str(0)
                }

class Login(Resource):
    def post(self):
        try:
            parser=reqparse.RequestParser()
            parser.add_argument('email',type=str)
            parser.add_argument('password', type=str)
            args = parser.parse_args()
            with db.atomic() as transaction:
                try:
                    query = MemberModel\
                    .select(MemberModel.password)\
                    .where(MemberModel.account == args['email'])

                    ok = False
                    for pw in query:
                        encoded_pw = hashlib\
                        .sha256( str(args['password']).encode()).hexdigest()
                        if encoded_pw == pw.password:
                            ok=True
                
                except Exception as e:
                    transaction.rollback()
                    return{
                        'error': str(e),
                        'email': args['email'],
                        'status': str(0)
                    }
            if ok:

                notice_dict_list=[]
                usr = MemberModel\
                    .select()\
                    .where(MemberModel.account == args['email'])
                
                for rrow in usr:
                    mem_id = rrow.id

                #Team, notice
                team_dict_list=[]

                query = InvolvedModel\
                    .select(InvolvedModel.g_id)\
                    .join(MemberModel)\
                    .where(MemberModel.id == mem_id)\
                    .distinct()

                for row in query:
                    info_query = GroupModel\
                    .select(GroupModel.id, GroupModel.name)\
                    .where(GroupModel.id == row.g_id)

                    for qqq in info_query:
                        ##qqq.id = team id
                        ##qqq.name = team name
                        num_query = InvolvedModel.select(fn.COUNT(InvolvedModel.m_id)).where(InvolvedModel.g_id==row.g_id)
                        team_dict_list.append(
                            {
                            'Team ID': qqq.id,
                            'Team Name':qqq.name,
                            'MemberNum': num_query.scalar()
                            }
                        )

                        notice_query = NoticeModel.select().where(qqq.id == NoticeModel.g_id)

                        for notice_row in notice_query:
                            notice_dict_list.append(
                                {
                                    "Team_id" : str(qqq.id),
                                    "Date": str(notice_row.created_at),
                                    "Text": notice_row.text,
                                }
                            )
                #User Info
                user_dict ={
                    "Email": "",
                    "Organization":"",
                    "Name":"",
                    "Schedule": [],
                }

                usr = MemberModel\
                    .select()\
                    .where(MemberModel.account == args['email'])

                for row in usr:
                    usr_id = row.id
                    usr_org= row.organization
                    usr_name=row.name

                schedule = TableBlankModel\
                    .select()\
                    .where(TableBlankModel.m_id == usr_id)
                
                user_dict['Email']=args['email']
                user_dict['Organization']=usr_org
                user_dict['Name'] = usr_name

                for row in schedule:
                    user_dict['Schedule'].append(str(row.day)+str(row.time))
                ret_team_dl = list(team_dict_list)
                ret_user_d  = dict(user_dict)
                ret_notice_dl=list(notice_dict_list)

                team_dict_list.clear()
                user_dict.clear()
                notice_dict_list.clear()
                return{
                    "Team":ret_team_dl,
                    "User":ret_user_d,
                    "Notice":ret_notice_dl,
                }


            else:
                return{
                    'email': args['email'],
                    'status': str(0)
                }

        except Exception as e:
            return{
                        'error': str(e),
                        'email': args['email'],
                        'status': str(0)
                    }
