from skateapp import app
from skateapp import database
from skateapp import config
import unittest
import os
import sqlite3
import json

class SkateAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(config.TestingConfig())
        self.database = database
        self.database.init_db()
        self.app = app.test_client()
        self.db_fd = os.open(app.config['DATABASE_URI'], os.O_CREAT)

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE_URI'])

    def test_insert_db(self):
        result = [1, unicode('name'), 100, 100, unicode('photo')]
        with app.app_context():
            self.database.query_db('insert into spots (name, latitude, longitude, photo) values (?, ?, ?, ?)', ['name', 100, 100, 'photo'])
            row = self.database.query_db('select * from spots')[0]
            res = [row[r] for r in row.keys()]
            assert res == result

    def test_delete_db(self):
        id = 1
        with app.app_context():
            self.database.query_db('insert into spots (name, latitude, longitude, photo) values (?, ?, ?, ?)', ['name', 100, 100, 'photo'])
            before = self.database.query_db('select * from spots')[0]
            self.database.query_db('delete from spots where id=?', [id])
            after = self.database.query_db('select * from spots')
            assert [before[r] for r in before.keys()] == [1, unicode('name'), 100, 100, unicode('photo')]
            assert after == []

    def test_home_page(self):
        rv = self.app.get('/')
        footer = 'background image'
        name = 'The Perfect Skate Spot'
        assert footer in rv.data
        assert name in rv.data

    def test_login_page(self):
        rv = self.app.get('/login')
        text = 'Login'
        footer = 'background image'
        assert footer in rv.data
        assert text in rv.data
        assert 'Username' in rv.data
        assert 'Password' in rv.data
        assert 'Sign in' in rv.data

    def test_api_spots(self):
        res = {}
        fakeshit = {"id":"1","name":"spot1","latitude": "100", "longitude": "100", "photo":"test/photo"}
        rv = self.app.get('/api/spots/')
        for line in rv.data.split('\n')[1:len(rv.data.split('\n'))-1]:
            key = line.split()[0].replace('"','').strip(':')
            val = line.split()[1].replace('"','').strip(',')
            res[key] = val
        assert json.dumps(fakeshit) == json.dumps(res)
        assert rv.content_type == 'application/json'

if __name__ == '__main__':
    unittest.main()
