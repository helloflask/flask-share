"""
    test_flask_share
    ~~~~~~~~~~~~~~~~
    Create social share component in Jinja2 template based on share.js.

    :author: Grey Li <withlihui@gmail.com>
    :copyright: (c) 2017 by Grey Li.
    :license: MIT, see LICENSE for more details.
"""
import unittest

from flask import Flask, render_template_string, current_app

from flask_share import Share


class ShareTestCase(unittest.TestCase):

    def setUp(self):
        self.mobile_agent = {'HTTP_USER_AGENT': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) \
        AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'}

        app = Flask(__name__)
        app.testing = True
        self.share = Share(app)

        @app.route('/')
        def index():
            return render_template_string('{{ share.load() }}\n{{ share.create() }}')

        self.context = app.app_context()
        self.context.push()
        self.client = app.test_client()

    def tearDown(self):
        self.context.pop()

    def test_config(self):
        self.assertIn('SHARE_SITES', current_app.config)
        self.assertIn('SHARE_MOBILE_SITES', current_app.config)
        self.assertIn('SHARE_HIDE_ON_MOBILE', current_app.config)
        self.assertIn('SHARE_SERVE_LOCAL', current_app.config)
        self.assertEqual(current_app.config['SHARE_HIDE_ON_MOBILE'], False)

    def test_load(self):
        rv = self.share.load()
        self.assertIn('https://cdn.bootcss.com', rv)
        self.assertIn('social-share.min.js', rv)

        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('social-share.min.js', data)

    def test_create(self):
        rv = self.share.create()
        self.assertIn('<div class="social-share', rv)

        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('<div class="social-share', data)

    def test_custom_sites(self):
        current_app.config['SHARE_SITES'] = 'twiter, facebook'
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('data-sites="twiter, facebook"', data)

    def test_custom_mobile_sites(self):
        current_app.config['SHARE_MOBILE_SITES'] = 'twitter'
        response = self.client.get('/', environ_base=self.mobile_agent)
        data = response.get_data(as_text=True)
        self.assertIn('data-mobile-sites="twitter"', data)

    def test_hide_on_mobile_config(self):
        current_app.config['SHARE_HIDE_ON_MOBILE'] = True
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('social-share.min.js', data)
        self.assertIn('<div class="social-share', data)

    def test_create_on_mobile(self):
        current_app.config['SHARE_HIDE_ON_MOBILE'] = True
        response = self.client.get('/', environ_base=self.mobile_agent)
        data = response.get_data(as_text=True)
        self.assertIn('social-share.min.js', data)
        self.assertNotIn('<div class="social-share', data)

    def test_local_resources(self):
        current_app.config['SHARE_SERVE_LOCAL'] = True

        response = self.client.get('/share/static/css/share.min.css')
        self.assertNotEqual(response.status_code, 404)

    def test_local_resources_on_dev(self):
        current_app.config['ENV'] = 'development'

        response = self.client.get('/share/static/css/share.min.css')
        self.assertNotEqual(response.status_code, 404)
