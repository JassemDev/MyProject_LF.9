import uuid
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)  # Aktiviert Cross-Origin Resource Sharing (CORS) für die App, um Anfragen von anderen Domains zuzulassen.

# Konfigurieren des Loggings
logging.basicConfig(level=logging.DEBUG)  # Setzt das Logging-Level auf DEBUG, um detaillierte Logs zu erhalten.

# Datenspeicher während der Laufzeit
todo_lists = {}  # Speichert die To-Do-Listen.
todo_entries = {}  # Speichert die Einträge der To-Do-Listen.

@app.before_request
def log_request():
    logging.debug(f'Request method: {request.method}, Path: {request.path}')  # Loggt Details zu jeder Anfrage.

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404  # Gibt einen 404-Fehler zurück, wenn eine Ressource nicht gefunden wird.

# Add some headers to allow cross-origin access to the API on this server, necessary for using
# Hinzufügen von CORS-Headern, um den Zugriff von anderen Domains zu erlauben (auskommentiert).
""" 
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, DELETE, PATCH'  # Achten Sie auf die korrekte Trennung mit Kommas
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response 
"""

# Hilfsfunktionen für die Fehlerbehandlung
def error_response(message, status_code):
    return jsonify({'error': message}), status_code  # Gibt eine JSON-Fehlermeldung mit einem Statuscode zurück.

def validate_list_id(list_id):
    return list_id in todo_lists  # Überprüft, ob eine Listen-ID existiert.

def validate_entry_id(list_id, entry_id):
    if list_id in todo_entries:
        return any(entry['id'] == entry_id for entry in todo_entries[list_id])  # Überprüft, ob eine Eintrags-ID existiert.
    return False

# Definiere Route für Hauptseite
@app.route('/')
@app.route('/todo-lists')
def index():
    return jsonify(list(todo_lists.values()))  # Gibt alle To-Do-Listen zurück.

@app.route('/todo-lists', methods=['GET'])
def get_all_lists():
    return jsonify(list(todo_lists.values()))  # Gibt alle To-Do-Listen zurück.

# Endpunkt zum Abrufen aller Einträge einer Liste
@app.route('/todo-list/<string:list_id>', methods=['GET'])
def get_list(list_id):
    if not validate_list_id(list_id):
        return error_response('Ungültige Listen-ID', 404)  # Gibt einen Fehler zurück, wenn die Listen-ID ungültig ist.
    return jsonify(todo_entries.get(list_id, []))  # Gibt alle Einträge einer Liste zurück.

# Endpunkt zum Löschen einer Liste
@app.route('/todo-list/<string:list_id>', methods=['DELETE'])
def delete_list(list_id):
    if not validate_list_id(list_id):
        return error_response('Ungültige Listen-ID', 404)  # Gibt einen Fehler zurück, wenn die Listen-ID ungültig ist.
    del todo_lists[list_id]
    del todo_entries[list_id]
    return jsonify({'message': 'Liste wurde gelöscht'}), 200  # Bestätigt das Löschen einer Liste.

# Endpunkt zum Hinzufügen einer Liste
@app.route('/todo-list', methods=['POST'])
def add_list():
    data = request.get_json()
    if not data or 'name' not in data:
        return error_response('Ungültige Listen-Daten', 406)  # Gibt einen Fehler zurück, wenn die Daten ungültig sind.
    list_id = str(uuid.uuid4())  # Generiert eine eindeutige ID für die Liste.
    todo_lists[list_id] = {'id': list_id, 'name': data['name']}  # Fügt die Liste hinzu.
    todo_entries[list_id] = []  # Initialisiert eine leere Eintragsliste.
    logging.debug(f"List added: {todo_lists[list_id]}")  # Loggt die hinzugefügte Liste.
    return jsonify(todo_lists[list_id]), 201  # Gibt die hinzugefügte Liste zurück.

# Endpunkt zum Hinzufügen eines Eintrags in eine Liste
@app.route('/todo-list/<string:list_id>/entry', methods=['POST'])
def add_entry(list_id):
    if not validate_list_id(list_id):
        return error_response('Ungültige Listen-ID', 404)  # Gibt einen Fehler zurück, wenn die Listen-ID ungültig ist.
    data = request.get_json()
    if 'name' not in data:
        return error_response('Ungültige Eintrags-Daten', 406)  # Gibt einen Fehler zurück, wenn die Eintrags-Daten ungültig sind.
    entry_id = str(uuid.uuid4())  # Generiert eine eindeutige ID für den Eintrag.
    data['id'] = entry_id
    if list_id not in todo_entries:
        todo_entries[list_id] = []
    todo_entries[list_id].append(data)  # Fügt den Eintrag zur Liste hinzu.
    return jsonify(data), 201  # Gibt den hinzugefügten Eintrag zurück.

# Endpunkt zum Aktualisieren eines Eintrags
@app.route('/todo-list/<string:list_id>/entry/<string:entry_id>', methods=['PATCH'])
def update_entry(list_id, entry_id):
    if not validate_entry_id(list_id, entry_id):
        return error_response('Eintrag nicht gefunden', 404)  # Gibt einen Fehler zurück, wenn der Eintrag nicht gefunden wurde.
    data = request.get_json()
    for entry in todo_entries[list_id]:
        if entry['id'] == entry_id:
            entry.update(data)  # Aktualisiert den Eintrag mit den neuen Daten.
            return jsonify(entry), 200  # Gibt den aktualisierten Eintrag zurück.
    return error_response('Eintrag nicht gefunden', 404)  # Gibt einen Fehler zurück, wenn der Eintrag nicht gefunden wurde.

# Endpunkt zum Löschen eines Eintrags
@app.route('/todo-list/<string:list_id>/entry/<string:entry_id>', methods=['DELETE'])
def delete_entry(list_id, entry_id):
    if not validate_entry_id(list_id, entry_id):
        return error_response('Eintrag nicht gefunden', 404)  # Gibt einen Fehler zurück, wenn der Eintrag nicht gefunden wurde.
    todo_entries[list_id] = [entry for entry in todo_entries[list_id] if entry['id'] != entry_id]  # Entfernt den Eintrag aus der Liste.
    return jsonify({'message': 'Eintrag gelöscht'}), 200  # Bestätigt das Löschen des Eintrags.

if __name__ == '__main__':
    # Startet den Flask-Server
    app.run(host='0.0.0.0', port=5000, debug=True)
