from skateapp import app
from views import *
from flask import json, make_response

@app.route('/api/add/', methods=['GET'])
def add_spot_page():
    return render_template('add.html')

@app.route('/api/update/', methods=['GET'])
def update_spot_page():
    return render_template('update.html')

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
    if cur:
        return json.jsonify(cur)
    else:
        abort(404)

@app.route('/api/spots/<id>', methods=['POST'])
def update_single_spot(id):
    eyed = id
    items = request.form.to_dict()
    avail = [k for k in items.keys() if items[k]]
    #dude, that's ugly. so many queries.
    cur = query_db('select * from spots where id=?',[eyed],one=True)
    if not cur:
        abort(404)
    for a in avail:
        try:
            #this doesn't seem secure
            g.db.execute('update spots set %s=? where id=?'%str(a), [items[a], eyed])
            g.db.commit()
        except sqlite3.Error, e:
            return e
    return redirect(url_for('get_single_spot', id=eyed))

@app.route('/api/spots/<id>', methods=['DELETE'])
def delete_single_spot(id):
    try:
        g.db.execute('delete from spots where id=?',[id])
        g.db.commit()
    except sqlite3.Error,e:
        return e
    return redirect(url_for('get_spots'))

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
