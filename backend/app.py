from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)  # Allow frontend to call this API

# MySQL connection config (set via environment variables in docker-compose)
def get_db_connection():
    return mysql.connector.connect(
        host='db',
        user='root',
        password='rootpassword',
        database='todos_db'
    )

@app.route('/api/todos', methods=['GET'])
def get_todos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM todos ORDER BY id DESC")
        todos = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(todos)
    except Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.json
    task = data.get('task')
    if not task:
        return jsonify({"error": "Task is required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO todos (task) VALUES (%s)", (task,))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"id": new_id, "task": task, "completed": False}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.json
    completed = data.get('completed')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE todos SET completed = %s WHERE id = %s", (completed, todo_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Updated"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
