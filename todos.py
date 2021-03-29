import time
import json
from datetime import datetime
import redis
from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
import sys
sys.path.append("../")
from helpers.pagination import Pagination

r = redis.Redis(host='redis', port=6379, decode_responses=True)

parser = reqparse.RequestParser()
parser.add_argument('task', required=False, help="Task cannot be blank!")
parser.add_argument('status', required=False)
parser.add_argument('page', required=False)
parser.add_argument('user_id', location='cookies')
parser.add_argument('session_id', location='cookies')

TodosUser = 'TodosUser'
TodosPrefix = 'todos:'
Username ='u1'

todo_u = TodosPrefix + Username

def abort_if_todo_doesnt_exist(todo):
    if not r.exists(todo):
        abort(404, message="Todo {} doesn't exist".format(todo))
        
def byte_to_list(b):
    return format(b).replace('"' and 'b', '').replace("'", '"').replace('"True"', 'true').replace('"False"', 'false')

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
        todo_user = todo_u + ':' +todo_id
        abort_if_todo_doesnt_exist(todo_user)
        data = r.hgetall(todo_user)
        if data:
            data['id'] = int(data['id'])
            data['status'] = True if data['status']=='True' else False
        return jsonify(data)

    def delete(self, todo_id):
        todo_user = todo_u + ':' +todo_id
        abort_if_todo_doesnt_exist(todo_user)
        r.delete( todo_user )
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        todo_user = todo_u + ':' +todo_id
        abort_if_todo_doesnt_exist(todo_user)
        data = r.hgetall(todo_user)
        newdata = {
            'status': args['status'] if args['status'] and args['status']!=data['status'] else data['status'],
            'task': args['task'] if args['task'] and args['task']!=data['task'] else data['task'],
            'updated_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        }
        r.hset(todo_user, None, None, newdata)
        newdata['status'] = True if newdata['status']=='True' else False
        return newdata, 201

class Todos(Resource):
        
    def get(self):
        TODOS = []
        args = parser.parse_args()
        total = r.zcount(TodosUser, '-inf', '+inf')
        page = args['page'] if args['page'] and int(args['page']) else 1;
        per_page = 9;
        start = ((int(page) - 1) * (per_page+1));
        end = per_page if start < per_page else start+per_page
        pagination = Pagination.getPager(total, int(page), per_page+1, 5)
        rtodos = r.zrange(TodosUser, start, end, desc=1, withscores=True)

        for todo in rtodos:
            data = r.hgetall(todo[0])
            if data:
                data['id'] = int(data['id'])
                data['status'] = True if data['status']=='True' else False
                TODOS.append(data)
        return jsonify({'todos': TODOS, 'pagination': pagination})

    def post(self):
        args = parser.parse_args()
        message = 0;
        if(not args['task'].isspace()):
            todo_id = r.zcount(TodosUser, '-inf', '+inf') + 1
            todo_user = todo_u + ':{}'.format(todo_id)
            data = {
                'id': int(todo_id),
                'task': args['task'],
                'status': 'True' if args['status'] else 'False',
                'created_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            }
            r.zadd(TodosUser, {todo_user: int(todo_id)})
            r.hset(todo_user, None, None, data)
            message = 1
        return message, 201
