from flask import request, jsonify, json

from storages import *
from application import app
from model import *


store = ToDoStorage()


@app.route('/')
def api():
    return 'This is the api for our little project'


@app.route('/todos', methods=['GET', 'POST'])
def todos():
    if request.method == 'GET':
        todo_list = store.list()
        return json.dumps(todo_list)
    else:
        new_todo = request.get_json()
        return jsonify(id=store.create(new_todo))


@app.route('/todos/<int:todo_id>', methods=['GET', 'PUT', 'DELETE'])
def todo(todo_id):
    if request.method == 'GET':
        return jsonify(store.get(todo_id))
    elif request.method == 'PUT':
        new_todo = request.get_json()
        if todo.id != todo_id:
            return "INVALID ID"
        else:
            store.update(todo)
            return "UPDATED"
    else:
        store.delete(todo_id)
        return 'DELETED'


@app.route('/login', methods=['POST'])
def login():
    user = request.get_json()
    # TODO: Set Cookie


#The following routes are to facilitate debugging
@app.route('/debug/populate', methods=['POST'])
def populate():
    todo_list = ['Arrive at venue', 'Listen to tutor', 'Do the Tutorial', 'Eat Pizza', 'Work on the project', 'Win']
    db.create_all()
    for todo in todo_list:
        item = Item(todo)
        db.session.add(item)
    db.session.commit()
    return jsonify(length=len(todo_list))


if __name__ == '__main__':
    debug = False
    # comment this out in production (you would (probably) want to have a config facility, in real life)
    debug = True
    app.run(debug=debug)
