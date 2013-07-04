import unittest

import flaskr


class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()

    def tearDown(self):
        pass

    def test_nothing(self):
        pass


if __name__ == '__main__':
    unittest.main()
