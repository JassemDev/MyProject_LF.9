import uuid
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS 

app = Flask(__name__)
CORS(app) 

# Konfigurieren des Loggings
logging.basicConfig(level=logging.DEBUG)

# Datenspeicher während der Laufzeit
todo_lists = {}
todo_entries = {}

@app.before_request
def log_request():
    logging.debug(f'Request method: {request.method}, Path: {request.path}')

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

# add some headers to allow cross origin acces to the API on this server, necessary for using
""" @app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, DELETE, PATCH'  # Achten Sie auf die korrekte Trennung mit Kommas
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response """

# Hilfsfunktionen für die Fehlerbehandlung
def error_response(message, status_code):
    return jsonify({'error': message}), status_code

def validate_list_id(list_id):
    return list_id in todo_lists

def validate_entry_id(list_id, entry_id):
    if list_id in todo_entries:
        return any(entry['id'] == entry_id for entry in todo_entries[list_id])
    return False

# definiere Route für Hauptseite
@app.route('/')
@app.route('/todo-lists')
def index():
    return jsonify(list(todo_lists.values()))

@app.route('/todo-lists', methods=['GET'])
def get_all_lists():
    return jsonify(list(todo_lists.values()))

# Endpunkt zum Abrufen aller Einträge einer Liste
@app.route('/todo-list/<string:list_id>', methods=['GET'])
def get_list(list_id):
    if not validate_list_id(list_id):
        return error_response('Ungültige Listen-ID', 404)
    return jsonify(todo_entries.get(list_id, []))

# Endpunkt zum Löschen einer Liste
@app.route('/todo-list/<string:list_id>', methods=['DELETE'])
def delete_list(list_id):
    if not validate_list_id(list_id):
        return error_response('Ungültige Listen-ID', 404)
    del todo_lists[list_id]
    del todo_entries[list_id]
    return jsonify({'message': 'Liste wurde gelöscht'}), 200

# Endpunkt zum Hinzufügen einer Liste
@app.route('/todo-list', methods=['POST'])
def add_list():
    data = request.get_json()
    if not data or 'name' not in data:
        return error_response('Ungültige Listen-Daten', 406)
    list_id = str(uuid.uuid4())
    todo_lists[list_id] = {'id': list_id, 'name': data['name']}
    todo_entries[list_id] = []
    logging.debug(f"List added: {todo_lists[list_id]}")  # Log the list that has been added
    return jsonify(todo_lists[list_id]), 201

# Endpunkt zum Hinzufügen eines Eintrags in eine Liste
@app.route('/todo-list/<string:list_id>/entry', methods=['POST'])
def add_entry(list_id):
    if not validate_list_id(list_id):
        return error_response('Ungültige Listen-ID', 404)
    data = request.get_json()
    if 'name' not in data:
        return error_response('Ungültige Eintrags-Daten', 406)
    entry_id = str(uuid.uuid4())
    data['id'] = entry_id
    if list_id not in todo_entries:
        todo_entries[list_id] = []
    todo_entries[list_id].append(data)
    return jsonify(data), 201

# Endpunkt zum Aktualisieren eines Eintrags
@app.route('/todo-list/<string:list_id>/entry/<string:entry_id>', methods=['PATCH'])
def update_entry(list_id, entry_id):
    if not validate_entry_id(list_id, entry_id):
        return error_response('Eintrag nicht gefunden', 404)
    data = request.get_json()
    for entry in todo_entries[list_id]:
        if entry['id'] == entry_id:
            entry.update(data)
            return jsonify(entry), 200
    return error_response('Eintrag nicht gefunden', 404)

# Endpunkt zum Löschen eines Eintrags
@app.route('/todo-list/<string:list_id>/entry/<string:entry_id>', methods=['DELETE'])
def delete_entry(list_id, entry_id):
    if not validate_entry_id(list_id, entry_id):
        return error_response('Eintrag nicht gefunden', 404)
    todo_entries[list_id] = [entry for entry in todo_entries[list_id] if entry['id'] != entry_id]
    return jsonify({'message': 'Eintrag gelöscht'}), 200

if __name__ == '__main__':
    # start Flask server
    app.run(host='0.0.0.0', port=5000, debug=True)
