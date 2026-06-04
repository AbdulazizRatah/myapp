import os
from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Retrieve database connection details from environment variables
DB_HOST = os.getenv("DB_HOST", "postgresql")
DB_NAME = os.getenv("DB_DATABASE", "myapp_db")
DB_USER = os.getenv("DB_USER", "db_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "db_password")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# 1. Define the function normally (without the broken decorator)
def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id SERIAL PRIMARY KEY,
            data TEXT NOT NULL
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/add', methods=['POST'])
def add_data():
    content = request.json.get('content')
    if not content:
        return jsonify({"error": "Missing content"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO entries (data) VALUES (%s);', (content,))
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"status": "Data inserted successfully!"}), 201

if __name__ == '__main__':
    # 2. Initialize the database using the app context before starting the server
    with app.app_context():
        create_tables()
        
    app.run(host='0.0.0.0', port=8080)
