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

        self.context = app.test_request_context()
        self.context.push()
        self.client = app.test_client()

    def tearDown(self):
        self.context.pop()

    def test_extension_exsit(self):  # need?
        assert 'share' in current_app.extensions

    def test_config(self):
        assert 'SHARE_SITES' in current_app.config
        assert 'SHARE_MOBILE_SITES' in current_app.config
        assert 'SHARE_HIDE_ON_MOBILE' in current_app.config
        assert current_app.config['SHARE_HIDE_ON_MOBILE'] == False

    def test_load(self):
        rv = self.share.load()
        assert 'https://cdn.bootcss.com' in rv
        assert 'social-share.min.js' in rv
        
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        assert 'social-share.min.js' in data

    def test_create(self):
        rv = self.share.create()
        assert '<div class="social-share' in rv

        response = self.client.get('/')
        data = response.get_data(as_text=True)
        assert '<div class="social-share' in data

    def test_custom_sites(self):
        current_app.config['SHARE_SITES'] = 'twiter, facebook'
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        assert 'data-sites="twiter, facebook"' in data

    def test_custom_mobile_sites(self):
        current_app.config['SHARE_MOBILE_SITES'] = 'twitter'
        response = self.client.get('/', environ_base=self.mobile_agent)
        data = response.get_data(as_text=True)
        assert 'data-mobile-sites="twitter"' in data

    def test_hide_on_mobile_config(self):
        current_app.config['SHARE_HIDE_ON_MOBILE'] = True
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        assert 'social-share.min.js' in data
        assert '<div class="social-share' in data

    def test_create_on_mobile(self):
        current_app.config['SHARE_HIDE_ON_MOBILE'] = True
        response = self.client.get('/', environ_base=self.mobile_agent)
        data = response.get_data(as_text=True)
        assert 'social-share.min.js' in data
        assert '<div class="social-share' not in data
