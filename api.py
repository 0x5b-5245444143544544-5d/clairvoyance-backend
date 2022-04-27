import json
from flask import Flask, jsonify
import database


app = Flask(__name__)
app.config["DEBUG"] = True

def get_current_temperature():
    db = database.Database().get()
    data = db['temperature'].find_one(order_by=['-id'])
    db.close()
    return data

@app.route('/current', methods=['GET'])
def current_temp():
    return jsonify(get_current_temperature())

@app.route('/history', methods=['GET'])
def history():
    return jsonify({"testing"})

app.run()