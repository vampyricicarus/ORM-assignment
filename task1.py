from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:your_password@localhost/fitness_center_db'
db = SQLAlchemy(app)

class Member(db.Model):
    __tableone__ = "Member"
    id = db.Column(db.Integer, primary_key=True)
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)

    class Fields:
        fields = ("name", "email", "phone", "id")

class WorkoutSession(db.Model):
    __tabletwo__ = "WorkoutSession"
    id = db.Column(db.Integer, primary_key=True)
    activity = fields.String(required=True)
    length = fields.Float(required=True)

@app.route('/members', methods=['POST'])
def add_member():
    try:
        conn = get_db_connection()
        if conn == None:
            return Jsonify("Error: connection failed"), 500
        cursor = conn.cursor()
        query = add_member("name", "age", "email")
        cursor.execute(query)
        cursor.commit()
        return members_schema.jsonify(members)
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    try:
        conn = get_db_connection()
        if conn == None:
            return Jsonify({"Error: connection failed"}), 500
        cursor = conn.cursor(dictionaries=True)

        query = "SELECT * FROM members"

        cursor.execute(query)

        return members_schema.jsonify(members)
    except Error as e:
        print(f"Error: {e}")
        return Jsonify({"Error Internal server error"})
    finally:
        if conn and conn.isconnected():
            cursor.close()
            conn.close()

@app.route(("/members/workout-sessions"), methods=["GET"])
def get_workout_session(id):
    try:
        conn = get_db_connection()
        if conn == None:
            return Jsonify({"Error: connection failed"}), 500
        cursor = conn.cursor(dictionaries=True)
        query = "SELECT * FROM WorkoutSession.ID"
        cursor.execute(query)
        return workout_session_schema.jsonify(id)
    finally:
        if conn and conn.isconnected():
            cursor.close()
            conn.close()

@app.route("/members/update", methods=["PUT"])
def update_member():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        data = request.json
        name, age, email = data["name"], data["age"], data["email"]
        name, age, email = request.json
        query = "UPDATE FROM members VALUES %s, %s, %s"
        cursor.execute(query, name, age, email)
        cursor.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

@app.route("/members/delete", methods=["DELETE"])
def delete_member():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "DELETE FROM members VALUES %s, %s, %s"
        cursor.execute(query, "name", "age", "email")
        cursor.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)