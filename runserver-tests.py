from skateapp import app
from skateapp import database
from skateapp import config
from flask import json
import unittest
import os
import sqlite3

# bro these are fugly
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
        footer = 'brian morrow'
        gh = 'github'
        assert footer in rv.data
        assert gh in rv.data

    def test_login_page(self):
        rv = self.app.get('/login')
        text = 'Login'
        footer = 'brian morrow'
        assert footer in rv.data
        assert text in rv.data
        assert 'Username' in rv.data
        assert 'Password' in rv.data
        assert 'Sign in' in rv.data

    def test_about_page(self):
        rv = self.app.get('/about')
        text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin diam enim, rutrum id lorem ut, pharetra varius arcu. Nulla pretium commodo turpis ut faucibus. Praesent euismod nunc quis elementum sodales. Maecenas tincidunt, sapien quis aliquet elementum, ipsum diam rutrum risus, ac auctor mi sem ut purus. Vestibulum odio tortor, vestibulum id urna ut, imperdiet facilisis purus. Nulla facilisi. Mauris blandit ultrices purus vel euismod.'
        assert rv.status_code == 200
        assert text in rv.data

    def test_api_get_all_spots(self):
        rv = self.app.get('/api/spots/')
        assert rv.data == '{\n  "results": []\n}'
        assert rv.content_type == 'application/json'

    def test_api_insert_spot(self):
        d = dict(name = 'test_spot',latitude = 69,longitude = 69,photo = 'test/path')
        notd = dict(name = 'test_spot1', latitude = 70, longitude = 70, photo = 'test/path1')
        rv = self.app.post('/api/spots/', data=d, follow_redirects=True)
        res = json.loads(rv.data)["results"][0]
        assert len(set(res.items()) & set(d.items())) == len(d)
        assert len(set(res.items()) & set(notd.items())) == 0
        assert rv.content_type == 'application/json'

    def test_api_get_single_spot(self):
        d = dict(name = 'test_spot',latitude = 69,longitude = 69,photo = 'test/path')
        notd = dict(name = 'test_spot1', latitude = 70, longitude = 70, photo = 'test/path1')

        post = self.app.post('/api/spots/', data=d, follow_redirects=True)
        id = str(json.loads(post.data)["results"][0]["id"])
        good = self.app.get('/api/spots/'+id)

        goodres = json.loads(good.data)
        assert good.status_code == 200
        assert good.content_type == 'application/json'
        assert len(set(goodres.items()) & set(d.items())) == len(d)
        assert len(set(goodres.items()) & set(notd.items())) == 0

    def test_api_delete_single_spot(self):
        d = dict(name = 'test_spot',latitude = 69,longitude = 69,photo = 'test/path')
        post = self.app.post('/api/spots/', data=d, follow_redirects=True)
        id = str(json.loads(post.data)["results"][0]["id"])
        self.app.delete('/api/spots/'+id)
        g = self.app.get('/api/spots/')
        assert g.data == '{\n  "results": []\n}'
        assert g.content_type == 'application/json'

    def test_api_update_single_spot(self):
        d = dict(name = 'test_spot',latitude = 69,longitude = 69,photo = 'test/path')
        newd = dict(name = 'new_test_spot')
        new2d = dict(name = 'newer_test_post', latitude = 30)
        post = self.app.post('/api/spots/', data=d, follow_redirects=True)
        id = str(json.loads(post.data)["results"][0]["id"])
        put = self.app.post('/api/spots/'+id, data=newd, follow_redirects=True)
        put2 = self.app.post('/api/spots/'+id, data=new2d, follow_redirects=True)
        putres = json.loads(put.data)
        put2res = json.loads(put2.data)
        assert put.status_code == 200
        assert put.content_type == 'application/json'
        assert len(set(putres.items()) & set(d.items())) == len(d) - 1
        assert len(set(putres.items()) & set(newd.items())) == 1

        assert len(set(put2res.items()) & set(d.items())) == len(d) - 2
        assert len(set(put2res.items()) & set(new2d.items())) == 2

    def test_all_404s(self):
        err = self.app.get('/asdf')
        assert err.status_code == 404
        assert '404' in err.data

        err = self.app.get('/api/spots/asdf')
        assert err.status_code == 404
        assert '404' in err.data

        err = self.app.post('/api/spots/nope',data=dict(),follow_redirects=False)
        assert err.status_code == 404
        assert '404' in err.data

if __name__ == '__main__':
    unittest.main()
