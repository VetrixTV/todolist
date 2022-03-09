import json
from uuid import uuid4

from flask import Flask, request

app = Flask(__name__)

user_id_bob = uuid4().__str__()
user_id_alice = uuid4().__str__()
user_id_eve = uuid4().__str__()
todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'
todo_1_id = uuid4().__str__()
todo_2_id = uuid4().__str__()
todo_3_id = uuid4().__str__()
todo_4_id = uuid4().__str__()

# define internal data structures with example data
user_list = [
    {'id': user_id_bob, 'name': 'Bob'},
    {'id': user_id_alice, 'name': 'Alice'},
    {'id': user_id_eve, 'name': 'Eve'},
]
todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
todos = [
    {'id': todo_1_id, 'name': 'Milch', 'description': '', 'list': todo_list_1_id, 'user': user_id_bob},
    {'id': todo_2_id, 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list': todo_list_2_id, 'user': user_id_alice},
    {'id': todo_3_id, 'name': 'Kinokarten kaufen', 'description': '', 'list': todo_list_3_id, 'user': user_id_eve},
    {'id': todo_3_id, 'name': 'Eier', 'description': '', 'list': todo_list_1_id, 'user': user_id_eve},
]


def listExists(list_id):
    """
    Checks if the given list_id exists
    :param list_id: the list_id
    :return: True if the list exists, False if not
    """
    for list in todo_lists:
        if list['id'] == list_id:
            return True
    return False


@app.route('/todo-list/<list_id>', methods=['GET'])
def getTodolist(list_id):
    """
    Gets a todolist based on the given list_id
    :param list_id: the list_id of the list you want
    :return: a List with all its entrys
    """
    if not listExists(list_id):
        return 'list does not exists', 404
    entrys = []
    for entry in todos:
        if entry["list"] == list_id:
            entrys.append(entry)
    return entrys.__str__()


@app.route('/todo-list/<list_id>/entry', methods=['PUT'])
def addEntry(list_id):
    """
    Adds the given entry to the given list
    {
        "name": "Entry01",
        "description": "Buy sand"
    }
    :param list_id: the list_id if the list
    :return: the added entry with all its data
    """
    if not listExists(list_id):
        return 'list does not exists', 404
    data = request.get_json()
    try:
        data['name']
        data['description']
    except KeyError:
        return 'missing data', 404
    entry = {'id': uuid4().__str__(),
             'name': data['name'],
             'description': data['description'],
             'user': '0',
             'list': list_id
             }
    todos.append(entry)
    return entry, 200


@app.route('/todo-list/<list_id>', methods=['DELETE'])
def deleteTodolist(list_id):
    """
    Deletes a todolist based on the list_id
    :param list_id: of the list you want to delete
    :return: 200 if the deleting was successful and 404 if not
    """
    index = None
    for list in todo_lists:
        if list['id'] == list_id:
            index = todo_lists.index(list)
            break
    if index != None:
        todo_lists.pop(index)
        return '', 200
    return '', 404


@app.route('/todo-list', methods=['POST'])
def createTodolist():
    """
    creates a todolist with the params in the body
    {
        "name": "The cool list"
    }
    :return: the created list
    """
    data = request.get_json()
    try:
        data['name']
    except KeyError:
        return 'missing data', 404
    todo_list = {'id': uuid4().__str__(),
                 'name': data['name'],
                 }
    todo_lists.append(todo_list)
    return todo_list, 200


@app.route('/todo-list/<list_id>/<entry_id>', methods=['PUT'])
def updateEntry(list_id, entry_id):
    """
    Updates a entry of a list, based on the data in the body
    {
        "name": "Entry 031314-Updated",
        "description": "Test Documentation"
    }
    :param list_id: of the list where the entry is in
    :param entry_id: the id of the entry
    :return: the changed entry, if it fails it returns 404 and entry not found
    """
    if not listExists(list_id):
        return 'list does not exists', 404
    data = request.get_json()
    try:
        data['name']
        data['description']
    except KeyError:
        return 'missing data', 404
    for entry in todos:
        if entry['id'] == entry_id:
            if entry["list"] == list_id:
                entry['name'] = data['name']
                entry['description'] = data['description']
                todos.insert(todos.index(entry), entry)
                return entry, 200
    return 'entry not found', 404


@app.route('/user', methods=['GET'])
def getAllUsers():
    """
    returns all the user
    :return: a list of all users
    """
    return json.loads(json.dumps(user_list.__str__())), 200


@app.route('/user', methods=['POST'])
def createUser():
    """
    Creates a User based on the params in the body
    {
        "name": "Peter"
    }
    :return: the created user
    """
    data = request.get_json()
    try:
        data['name']
    except KeyError:
        return 'missing data', 404
    user = {
        'id': uuid4().__str__(),
        'name': data['name']
    }
    user_list.append(user)
    return user


@app.route('/user/<user_id>', methods=['DELETE'])
def deleteUser(user_id):
    """
    deletes the user based on the id
    :param user_id: id of the user
    :return: 200 if the user was found and deleted, 404 if the user was not found and not deleted
    """
    index = None
    for user in user_list:
        if user['id'] == user_id:
            index = user_list.index(user)
            break
    if index != None:
        user_list.pop(index)
        return '', 200
    return '', 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=1)
