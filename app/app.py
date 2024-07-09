from flask import Flask, request, jsonify, make_response
import mysql.connector
import os
import datetime
import socket

app = Flask(__name__)

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'db'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', 'root_password'),
            database=os.getenv('DB_NAME', 'app_db')
        )
        return connection
    except mysql.connector.Error as err:
        app.logger.error(f"Database connection error: {err}")
        return None

@app.route('/')
def index():
    db = get_db_connection()
    if not db:
        return make_response("Database connection failed", 500)

    cursor = db.cursor()

    try:
        cursor.execute("UPDATE global_counter SET counter_value = counter_value + 1")
        db.commit()

        cursor.execute("SELECT counter_value FROM global_counter")
        counter_value = cursor.fetchone()[0]

        client_ip = request.remote_addr
        internal_ip = socket.gethostbyname(socket.gethostname())  # Get the internal IP address
        request_time = datetime.datetime.now()

        cursor.execute("INSERT INTO access_log (request_time, client_ip, internal_ip) VALUES (%s, %s, %s)",
                       (request_time, client_ip, internal_ip))
        db.commit()
    except mysql.connector.Error as err:
        app.logger.error(f"SQL error: {err}")
        db.close()
        return make_response("Database query failed", 500)

    db.close()

    response = jsonify(internal_ip=internal_ip)
    if not request.cookies.get('session_id'):
        response.set_cookie('session_id', internal_ip, max_age=300)
    return response

@app.route('/showcount')
def showcount():
    db = get_db_connection()
    if not db:
        return make_response("Database connection failed", 500)

    cursor = db.cursor()

    try:
        cursor.execute("SELECT counter_value FROM global_counter")
        counter_value = cursor.fetchone()[0]
    except mysql.connector.Error as err:
        app.logger.error(f"SQL error: {err}")
        db.close()
        return make_response("Database query failed", 500)

    db.close()
    return jsonify(counter_value=counter_value)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

