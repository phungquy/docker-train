import os
import time
import json
from datetime import datetime
import redis
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from flask_paginate import Pagination, get_page_parameter

FB_CLIENT_ID = os.environ.get("FB_CLIENT_ID")
FB_CLIENT_SECRET = os.environ.get("FB_CLIENT_SECRET")

FB_AUTHORIZATION_BASE_URL = "https://www.facebook.com/dialog/oauth"
FB_TOKEN_URL = "https://graph.facebook.com/oauth/access_token"

FB_SCOPE = ["email"]

# This allows us to use a plain HTTP callback
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = Flask(__name__)
api = Api(app)

r = redis.Redis(host='redis', port=6379)

parser = reqparse.RequestParser()
parser.add_argument('task', required=False, help="Task cannot be blank!")
parser.add_argument('status', required=False)
parser.add_argument('page', required=False)
parser.add_argument('user_id', location='cookies')
parser.add_argument('session_id', location='cookies')
TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}
TodosUser = 'TodosUser'
TodosPrefix = 'todos:'
Username ='u1'
class User:
    def login():
        facebook = requests_oauthlib.OAuth2Session(
            FB_CLIENT_ID, redirect_uri=URL + "/fb-callback", scope=FB_SCOPE
        )
        authorization_url, _ = facebook.authorization_url(FB_AUTHORIZATION_BASE_URL)
        return flask.redirect(authorization_url)

    def create_user(**data):
        # Creates user with encrypted password
        if 'username' not in data or 'password' not in data:
            raise ValueError('username and password are required.')
        data['password'] = generate_password_hash(
            data.pop('password'),
            method='pbkdf2:sha256'
        )
        # store user at users:{username}
        r.hmset('users:{}'.format(data['username']), data)
        h.save()
        return data

    def putvalidate_login(user):
        if not r.exists('users:{}'.format(user['username'])):
            return False
        stored_password = r.hget('users:{}'.format(user['username']), 'password')
        if check_password_hash(stored_password, user['password']):
            return True
        return False
    def configure_extensions(app):
        sl = SimpleLogin(app, login_checker=validate_login)

todo_u = TodosPrefix + Username

def abort_if_todo_doesnt_exist(todo):
    if not r.exists(todo):
        abort(404, message="Todo {} doesn't exist".format(todo))
        
def byte_to_list(b):
    return format(b).replace('"' and 'b', '').replace("'", '"') 

class Test(Resource):
    def get(self):
        count = self.get_hit_count()
        return 'Hello from Python - Flask! I have been seen {} times.'.format(count)

    def get_hit_count(self):
        retries = 5
        while True:
            try:
                return r.incr('hits')
            except redis.exceptions.ConnectionError as exc:
                if retries == 0:
                    raise exc
                retries -= 1
                time.sleep(0.5)

# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        TODO = {}
        todo_user = todo_u + ':' +todo_id
        abort_if_todo_doesnt_exist(todo_user)
        TODO[todo_user] = json.loads(byte_to_list(r.hgetall(todo_user)))
        return jsonify(TODO)

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        todo_user = todo_u + ':' +todo_id
        abort_if_todo_doesnt_exist(todo_user)
        r.hset(todo_user, 'status', args['status'])
        r.hset(todo_user, 'updated_at', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
        return True, 201

class Todos(Resource):
    def get(self):
        TODOS = {}
        args = parser.parse_args()
        page = args['page'];
        pagination = Pagination(page=page, total=users.count(), search=search, record_name='users')
        rtodos = byte_to_list(r.lrange(TodosUser, 0, 9))     
        LIST_TODOS = json.loads(rtodos)
        for i in LIST_TODOS:
            TODOS[i] = json.loads(byte_to_list(r.hgetall(i)))
        return jsonify(TODOS)

    def post(self):
        args = parser.parse_args()
        if(args['status']): args['status'] = 'True'
        else: args['status'] = 'False'
        todo_id = r.llen(TodosUser)+1
        todo_user = todo_u + ':{}'.format(todo_id)
        r.lpush(TodosUser, todo_user)
        r.hset(todo_user, 'task', args['task'])
        r.hset(todo_user, 'status', args['status'])
        r.hset(todo_user, 'created_at', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
        r.hset(todo_user, 'updated_at', datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))
        return todo_user, 201

api.add_resource(Test, '/api')
api.add_resource(Todos, '/api/todos')
api.add_resource(Todo, '/api/todos/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
