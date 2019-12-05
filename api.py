
from flask import Flask,url_for,redirect,abort
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

class NullPage(Resource):
    def get(self):
        return redirect('https://atez.kagamine.me/',code=302)

api.add_resource(NullPage, '/')
api.add_resource(CreateUser, '/add_user')
api.add_resource(DeleteUser, '/withdrawl')


api.add_resource(Login, '/login')
api.add_resource(CreateGroup, '/team_enroll')
api.add_resource(DeleteGroup, '/team_delete')

api.add_resource(TeamManage, '/team_manage')
api.add_resource(ReadTeam, '/read_team')

api.add_resource(AddTimeTable, '/add_schedule')
api.add_resource(ChangeTimeTable, '/delete_schedule')
api.add_resource(GetMaxTeamId, '/get_max_team_id')

api.add_resource(MemberSearch, '/member_search')
api.add_resource(ReadUser, '/read_member')
 
api.add_resource(WriteNotice, '/add_notice')
api.add_resource(DeleteNotice, '/delete_notice')
api.add_resource(UpdateNotice, '/update_notice')


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
	debug=True,
        )
