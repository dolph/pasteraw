import unittest
import uuid

import pasteraw


class PasterawTestCase(unittest.TestCase):
    def setUp(self):
        pasteraw.app.config['TESTING'] = True
        pasteraw.app.config['CSRF_ENABLED'] = False
        self.app = pasteraw.app.test_client()

    def tearDown(self):
        pass

    def assertRedirect(self, response, location):
        self.assertIn(response.status_code, (301, 302))
        self.assertEqual(response.location, 'http://localhost' + location)

    def test_favicon(self):
        r = self.app.get('/favicon.ico')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.content_type, 'image/x-icon')
        self.assertIn('public', r.cache_control)

    def test_static_favicon(self):
        r = self.app.get('/static/favicon.ico')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.content_type, 'image/x-icon')
        self.assertIn('public', r.cache_control)

    def create_paste(self, content, follow_redirects=False):
        return self.app.post(
            '/',
            data={'content': content},
            follow_redirects=follow_redirects)

    def test_create_paste(self):
        content = uuid.uuid4().hex
        r = self.create_paste(content, follow_redirects=True)
        self.assertEquals(r.data, content)

    def test_create_paste_without_content(self):
        r = self.create_paste(content='')
        self.assertIn('This field is required.', r.data)

    def test_create_paste_predictable_url(self):
        """URL's are just base-36 encoded SHA-1 hashes of the content."""
        r = self.create_paste(
            content='2y0txsm7ikq0cykn79dzg1rcs')
        self.assertRedirect(r, '/odvznvo86eyb44mr06ditj55jtears6')

    def test_create_paste_idempotent(self):
        content = uuid.uuid4().hex
        r1 = self.create_paste(content)
        r2 = self.create_paste(content)
        self.assertEquals(r1.location, r2.location)


if __name__ == '__main__':
    unittest.main()
