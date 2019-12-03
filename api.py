
from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse

from service.UserService import *
from service.GroupService import *
from service.TimeTableService import *
from service.NoticeService import *

from extension import mydb
from model import *

app = Flask(__name__)
api = Api(app)
db = mydb

api.add_resource(CreateUser, '/add_user')
api.add_resource(Login, '/login')
api.add_resource(CreateGroup, '/team_enroll')
api.add_resource(DeleteGroup, '/team_delete')
api.add_resource(DeleteUser, '/withdrawl')


api.add_resource(TeamManage, '/team_manage')
api.add_resource(ChangeTimeTable, '/update_schelude')
api.add_resource(ReadTeam, '/read_team')
api.add_resoruce(ChangeTimeTable, '/update_schelude')
api.add_resource(GetMaxTeamId, '/get_max_team_id')

api.add_resource(MemberSearch, '/member_search')
api.add_resource(ReadUser, '/read_member')

api.add_resource(WriteNotice, '/add_notice')

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        )
    #app.run(debug=True)
