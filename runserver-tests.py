from skateapp import app
import unittest
import os
class SkateAppTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd = os.open(app.config['DATABASE_URI'], os.O_CREAT)
        self.app = app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE_URI'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'Nothing here.' in rv.data

if __name__ == '__main__':
    unittest.main()
