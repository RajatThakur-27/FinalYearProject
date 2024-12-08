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

def connect_to_db(config):
    """Create database connection"""
    try:
        connection = mysql.connector.connect(**config)
        print("Connection successful")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

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

def check_status_in_db2(roll_number):
    """Check status in database 2"""
    connection = connect_to_db(db_config)
    if not connection:
        return None
    
    cursor = connection.cursor()
    try:
        query = "SELECT EXISTS(SELECT 1 FROM students_status WHERE roll_number = %s)"
        cursor.execute(query, (roll_number,))
        result = cursor.fetchone()[0]
        if result==0:
            query = """
            INSERT INTO students_status 
            (roll_number) 
            VALUES (%s)
            """
            values = (
                roll_number,
            )
            cursor.execute(query, values)
            connection.commit()
        query = "SELECT entry_id FROM students_status WHERE roll_number = %s"
        cursor.execute(query, (roll_number,))
        result = cursor.fetchone()
        return result[0] if result else None
    except mysql.connector.Error as err:
        print(f"Error checking status: {err}")
        return None
    finally:
        cursor.close()
        connection.close()

def create_entry_in_db3(roll_number, parameters):
    """Create new entry in table 3"""
    connection = connect_to_db(db_config)
    if not connection:
        return False
    
    cursor = connection.cursor()
    try:
        query = "SELECT name FROM students_data WHERE roll_no = %s"
        cursor.execute(query, (roll_number,))
        name = cursor.fetchone()[0]
        query = """
        INSERT INTO enteries 
        (roll_number,name,  entry_type, first_location, first_entry_date, first_entry_time) 
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            roll_number,
            name,
            parameters.get('parameter1'),
            parameters.get('parameter2'),
            datetime.now(),
            datetime.now().date,
        )
        cursor.execute(query, values)
        connection.commit()
        query = "SELECT id FROM enteries WHERE roll_no = %s"
        cursor.execute(query, (roll_number,))
        index = cursor.fetchone()[0]
        # storing the entry id in students status table
        query = """
        UPDATE enteries 
        SET entry_id
        WHERE roll_number = %s
        """
        values = (
            index,
        )
        cursor.execute(query, values)
        connection.commit()

        return True
    except mysql.connector.Error as err:
        print(f"Error creating entry: {err}")
        return False
    finally:
        cursor.close()
        connection.close()

# def complete_entry_in_db3(roll_number, parameters):
#     """Complete existing entry in database 3 and update status"""
#     connection = connect_to_db(db_config)
#     if not connection:
#         return False
    
#     cursor = connection.cursor()
#     try:
#         # Update the existing entry
#         query = """
#         UPDATE enteries 
#         SET parameter3 = %s, 
#             parameter4 = %s, 
#             completion_date = %s,
#             status = %s 
#         WHERE roll_number = %s AND status = TRUE
#         """
#         values = (
#             parameters.get('parameter3'),
#             parameters.get('parameter4'),
#             datetime.now(),
#             False,
#             roll_number
#         )
#         cursor.execute(query, values)
#         connection.commit()
#         return True
#     except mysql.connector.Error as err:
#         print(f"Error completing entry: {err}")
#         return False
#     finally:
#         cursor.close()
#         connection.close()

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
        if not check_roll_number_validity(roll_number):
            return jsonify({'status': 'error', 'message': 'Invalid roll number'}), 400

        # Step 2: Check status in DB2
        status = check_status_in_db2(roll_number)
        if status is None:
            return jsonify({'status': 'error', 'message': 'Error checking status'}), 500

        # Step 3: Handle DB3 operations based on status
        if status == -1 :
            # Create new entry
            if create_entry_in_db3(roll_number, parameters):
                return jsonify({'status': 'success', 'message': 'New entry created'}), 200
        # else:
        #     # Complete existing entry
        #     if complete_entry_in_db3(roll_number, parameters):
        #         return jsonify({'status': 'success', 'message': 'Entry completed'}), 200

        return jsonify({'status': 'error', 'message': 'Operation failed'}), 500

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route("/") 
def index(): 
    return "Homepage of GeeksForGeeks"

app.run(host="localhost", port=5000, debug=True)
if __name__ == '_main_':
    app.run(debug=True)