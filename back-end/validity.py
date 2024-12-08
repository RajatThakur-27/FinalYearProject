from flask import Flask, request, jsonify
from flask_cors import CORS 

import mysql.connector
from datetime import datetime

app = Flask(__name__)
CORS(app)

# app.run(host="localhost", port=5000, debug=True)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Database connection configurations
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Project@48',
    'database': 'students-enteries'
}

name = "default"

# Creating database connection
def connect_to_db(config):
    """Create database connection"""
    try:
        connection = mysql.connector.connect(**config)
        print("Connection successful")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

# Checking validity of roll number
def check_roll_number_validity(roll_number):
    """Check if roll number exists in database 1"""
    connection = connect_to_db(db_config)
    if not connection:
        return False
    
    cursor = connection.cursor()
    try:
        query = "SELECT EXISTS(SELECT 1 FROM students_data WHERE roll_no = %s)"
        cursor.execute(query, (roll_number,))
        result = cursor.fetchone()[0]
        return bool(result)
    except mysql.connector.Error as err:
        print(f"Error checking roll number: {err}")
        return False
    finally:
        cursor.close()
        connection.close()

# Accessing the status of student entry by retrieving the index from database 1
def check_index_in_db1(roll_number):
    """Check status in database 2"""
    connection = connect_to_db(db_config)
    if not connection:
        return None
    
    cursor = connection.cursor()
    try:
        query = "SELECT index FROM students_data WHERE roll_number = %s"
        cursor.execute(query, (roll_number,))
        result = cursor.fetchone()
        return result[0] if result else None
    except mysql.connector.Error as err:
        print(f"Error checking status: {err}")
        return None
    finally:
        cursor.close()
        connection.close()

@app.route('/submit-form', methods=['POST'])
def handle_form_submission():
    try:
        data = request.get_json()
        roll_number = data.get('roll_number')
        parameters = {
            'parameter1': data.get('parameter1'),
            'parameter2': data.get('parameter2')
        }

        # Step 1: Check roll number validity in DB1
        # Step 2: If roll number is valid then it will return the 
        if not check_roll_number_validity(roll_number):
            return jsonify({'status': 'error', 'message': 'Invalid roll number'}), 400
        
        # Step 3: Retrieve the index of roll number from DB1
# cal check_index_in_db1(roll_number) function and return the index
        id = check_index_in_db1(roll_number)
        if id == -1:
            # will make first entry by calling its function
        else:
            # will make second entry by calling its function

        return jsonify({'status': 'success', 'message': 'Entered Roll Number is valid'}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route("/") 
def index(): 
    return "Homepage of GeeksForGeeks"

app.run(host="localhost", port=5000, debug=True)
if __name__ == '_main_':
    app.run(debug=True)