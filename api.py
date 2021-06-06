from get_route import GetRoute
from flask import Flask
from flask import request
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)
# Инициализирую клас Маршрутов, что бы прогрузились
# все карты маршрутов, что бы не ждать каждый раз
# когда нужно просчитать маршрут
route = GetRoute()

@app.route('/getRoute', methods=['GET', ])
def my_route():
    longitude = request.args.get('longitude')
    latitude = request.args.get('latitude')
    # Запускаю просчет маршрута по координатам
    route.getRoteData(float(longitude), float(latitude))
    # Возращаю лист координатов
    return route.dataJson

# TODOS = {
#     'todo1': {'task': 'build an API'},
#     'todo2': {'task': '?????'},
#     'todo3': {'task': 'profit!'},
# }


# def abort_if_todo_doesnt_exist(todo_id):
#     if todo_id not in TODOS:
#         abort(404, message="Todo {} doesn't exist".format(todo_id))

# parser = reqparse.RequestParser()
# parser.add_argument('task')


# # Todo
# # shows a single todo item and lets you delete a todo item
# class Todo(Resource):
#     def get(self, todo_id):
#         abort_if_todo_doesnt_exist(todo_id)
#         return TODOS[todo_id]

#     def delete(self, todo_id):
#         abort_if_todo_doesnt_exist(todo_id)
#         del TODOS[todo_id]
#         return '', 204

#     def put(self, todo_id):
#         args = parser.parse_args()
#         task = {'task': args['task']}
#         TODOS[todo_id] = task
#         return task, 201


# # TodoList
# # shows a list of all todos, and lets you POST to add new tasks
# class TodoList(Resource):
#     def get(self):
#         return TODOS

#     def post(self):
#         args = parser.parse_args()
#         todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
#         todo_id = 'todo%i' % todo_id
#         TODOS[todo_id] = {'task': args['task']}
#         return TODOS[todo_id], 201

# # GetRoute
# # shows a list of all todos, and lets you POST to add new tasks
# class GetRoute(Resource):
    
#     def get(self):
#         longitude = app.args.get('longitude')
#         latitude = app.args.get('latitude')
#         # Запускаю просчет маршрута по координатам
#         route.getRoteData(longitude, latitude)
#         # Возращаю лист координатов
#         return route.dataJson
      

# ##
# ## Actually setup the Api resource routing here
# ##
# api.add_resource(TodoList, '/todos')
# api.add_resource(Todo, '/todos/<todo_id>')
# api.add_resource(GetRoute, '/getRoute')


if __name__ == '__main__':
    app.run(debug=True)