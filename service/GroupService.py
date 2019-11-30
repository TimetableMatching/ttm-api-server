from flask_restful import Resource, Api
from flask_restful import reqparse
from extension import mydb
from model import *

db = mydb

class CreateGroup(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str)
            args = parser.parse_args()

            with db.atomic() as transaction:
                try:
                    GroupModel.create(
                        name = str(args['name']),
                    )
                except Exception as e:
                    transaction.rollback()
                    return{
                        'result_message': 'DB:'+str(e),
                        'status' : str(0)
                    }

            return {
                'name': args['name'],
                'status': str(1),
                'result_message': 'success',
            }
        except Exception as e:
            return {
                'error': str(e),
                'status': str(0)
                }

class TeamManage(Resource):
    def post(self):
        try:
            parser=reqparse.RequestParser()
            parser.add_argument('email',type=str)
            args = parser.parse_args()
            with db.atomic() as transaction:
                try: 
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
                                'MemberNum': str(num_query.scalar())
                                }
                            )

                    return {
                        "Team":team_dict_list,
                    }

                except Exception as e:
                    return {
                        "error":str(e),
                        "status":str(0)
                    }
        except Exception as e:
             return {
                        "error":str(e),
                        "status":str(0)
                    }

class ReadTeam(Resource):
    def post(self):
        ERROR_DICT = {
                "error":"",
                "status":str(0)
            }
        try:
            result_dict={
                "Team ID":"",
                "Team Name":"",
                "MemberNum":"",
                "Member":[],
                "notice":[],
            }

            parser = reqparse.RequestParser()
            parser.add_argument('team_id', type=str)
            args = parser.parse_args()

            # Team ID가 주어지면, groups 테이블에서 Name
            with db.atomic() as transaction:
                try:
                    #Team
                    name_query = GroupModel\
                        .select(GroupModel.name)
                    for row in name_query:
                        group_name = row.name
                    
                    members = InvolvedModel\
                        .select(InvolvedModel.m_id, MemberModel.account, MemberModel.name, MemberModel.organization)\
                        .join(MemberModel)\
                        .where(InvolvedModel.g_id == args['team_id'])\
                        .dicts()
                    result_dict['Team ID'] = args['team_id']
                    result_dict['Team Name'] = group_name
                    mem_num=0


                    for mem in members:
                        mem_num+=1

                        tt_list= []
                        time_table_query = TableBlankModel\
                            .select(TableBlankModel.day,TableBlankModel.time)\
                            .where(TableBlankModel.m_id == mem['m_id'])\
                            .dicts()
                        
                        for tt in time_table_query:
                            tt_list.append(str(tt['day'])+str(tt['time']))
                        result_dict["Member"].append(
                            {
                                "Email":str(mem['account']),
                                "Organization":str(mem['organization']),
                                "Name":str(mem['name']),
                                "Schedule":tt_list,
                            }
                        )
                    
                    result_dict['MemberNum'] = mem_num

                    notice_query = NoticeModel\
                        .select()\
                        .where(NoticeModel.g_id==args['team_id'])\
                        .dicts()
                    
                    for notice_row in notice_query:
                        print(notice_row)
                        result_dict['notice'].append(
                            {
                                "Team_id" : str(args['team_id']),
                                "Date" : str(notice_row['created_at']),
                                "Text" : str(notice_row['text']),
                                "author":str(notice_row['author']),
                            }
                        )
                    
                    return result_dict
                    

                except Exception as e:
                    ERROR_DICT['error']=str(e)
                    return ERROR_DICT

        except Exception as e:
            ERROR_DICT['error']=str(e)
            return ERROR_DICT   