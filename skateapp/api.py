from skateapp import app
from views import *
from flask import json, make_response

@app.route('/api/add/', methods=['GET'])
def add_spot_page():
    return render_template('add.html')

def dict_from_row(row):
    return dict(zip(row.keys(), row))

@app.route('/api/spots/', methods=['GET'])
def get_spots():
    cur = query_db('select * from spots')
    d = []
    for a in cur:
        d.append(dict(a))
    return json.jsonify(results=d)

@app.route('/api/spots/<id>', methods=['GET'])
def get_single_spot(id):
    cur = query_db('select * from spots where id=?',[id],one=True)
    return json.jsonify(cur)

@app.route('/api/spots/', methods=['POST'])
def add_spot():
    items = request.form.to_dict()
    its = [items["name"], int(items["latitude"]), int(items["longitude"]), items["photo"]]
    try:
        g.db.execute('''insert into spots (name, latitude, longitude, photo) values (?, ?, ?, ?)''', its)
        g.db.commit()
    except sqlite3.Error,e:
        return e
    return redirect(url_for('get_spots'))
