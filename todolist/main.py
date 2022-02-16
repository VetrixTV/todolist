from uuid import uuid4

from flask import Flask, request

app = Flask(__name__)

new_entry = {'id': '1a5eebec-410d-4904-8599-71244fbb25cb',
             'name': 'Milch einkaufen',
             'description': '',
             'user_id': 'e302b6b8-65d0-48b1-a1b3-1e40307ebf51',
             'list_id': 'c819997b-9b75-44a6-95e1-79da9ed36170'}

list_entries = []

list_entries.append(new_entry)

todo_list = []

todo_list.append("c819997b-9b75-44a6-95e1-79da9ed36170")


@app.route('/todo-list/<list_id>', methods=['GET'])
def getTodolist(list_id):
    try:
        todo_list.index(list_id)
    except ValueError:
        return "THAT LIST WAS NOT FOUND!"
    entrys = []
    # TODO: fix the search, this is just slow itself
    for entry in list_entries:
        if entry["list_id"] == list_id:
            entrys.append(entry)
    return entrys.__str__()


@app.route('/todo-list/<list_id>/entry', methods=['PUT'])
def addEntry(list_id):
    try:
        todo_list.index(list_id)
    except ValueError:
        return '', 404
    data = request.get_json()
    try:
        data['name']
        data['description']
    except KeyError:
        return 'missing data', 404
    entry = {'id': uuid4(),
             'name': data['name'],
             'description': data['description'],
             'user_id': '0',
             'list_id': list_id
             }
    list_entries.append(entry)
    return '', 200


@app.route('/todo-list/<list_id>', methods=['DELETE'])
def deleteTodolist(list_id):
    return f'your trying to delete the todo-list {list_id}'


@app.route('/todo-list', methods=['POST'])
def createTodolist():
    return f'your trying to create a todo-list'


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=1)
