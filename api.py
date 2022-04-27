import json
from flask import Flask, jsonify
from flask_cors import CORS
import database


app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

def get_current_temperature():
    db = database.Database().get()
    data = db['temperature'].find_one(order_by=['-id'])
    db.close()
    return data

def get_temperature_history():
    db = database.Database().get()
    data = db['temperature'].find(limit=50)
    db.close()
    return [dict(id=result['id'], temperature=result['temperature'], timestamp=result['timestamp']) for result in data]

@app.route('/current', methods=['GET'])
def current_temp():
    response = jsonify(get_current_temperature())
    response.access_control_allow_origin = '*'
    return response

@app.route('/history', methods=['GET'])
def history():
    return jsonify(get_temperature_history())

app.run()