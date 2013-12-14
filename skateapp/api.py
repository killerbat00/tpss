from skateapp import app
from views import *
from flask import jsonify

fakeshit = {"id":1,"name":"spot1","latitude":100,"longitude":100,"photo":"test/photo"}

@app.route('/api/spots/', methods=['GET'])
def get_spots():
    return jsonify(**fakeshit)
