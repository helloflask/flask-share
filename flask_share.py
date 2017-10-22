# -*- coding: utf-8 -*-
"""
    Flask-Share
    ~~~~~~~~~~~~~~
    Create social share component in Jinja2 template based on share.js.
    :copyright: (c) 2017 by Grey Li.
    :license: MIT, see LICENSE for more details.
"""
import re

from flask import current_app, Markup, request


class Share(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['share'] = self

        # app.context_processor(self.context_processor)
        app.context_processor(lambda: {'share': current_app.extensions['share']})
        # app.add_template_global()
        # app.jinja_env.globals['csrf_token'] = generate_csrf

        # default settings
        app.config.setdefault('SHARE_SITES', 'weibo, wechat, douban, facebook,\
         twitter, google, linkedin, qq, qzone')
        app.config.setdefault('SHARE_MOBILE_SITES', 'weibo, douban, qq, qzone')
        app.config.setdefault('SHARE_HIDE_ON_MOBILE', False)

    @staticmethod
    def context_processor():
        return {'share': current_app.extensions['share']}

    @staticmethod
    def load(css_url=None, js_url=None):
        """Load share.js resource from CDN.

        :param css_url: if set, will be used as css url.
        :param js_url: if set, will be used as js url.
        """
        if css_url is None:
            css_url = 'https://cdn.bootcss.com/social-share.js/1.0.16/css/share.min.css'
        if js_url is None:
            js_url = 'https://cdn.bootcss.com/social-share.js/1.0.16/js/social-share.min.js'
        return Markup('''<link rel="stylesheet" href="%s" type="text/css">\n
            <script src="%s"></script>''' % (css_url, js_url))

    @staticmethod
    def create(title='', sites=None, mobile_sites=None, align='left', addition_class=''):
        """Create a share component.

        :param title: the prompt dispalyed on the left of the share component.
        :param sites: a string that consist of sites, separate by comma.
                      supported site name: weibo, wechat, douban, facebook, twitter,
                      google, linkedin, qq, qzone.
                      for example: `'weibo, wechat, qq'`.
        :param mobile_sites: the sites displayed on mobile.
        :param align: the align of the share component, default to `'left'`.
        :param addition_class: the style class added to the share component.
        """
        if current_app.config['SHARE_HIDE_ON_MOBILE']:
            platform = request.user_agent.platform
            if platform is not None:
                mobile_pattern = re.compile('android|fennec|iemobile|iphone|opera (?:mini|mobi)')
                m = re.match(mobile_pattern, platform)
                if m is not None:
                    return ''

        if sites is None:
            sites = current_app.config['SHARE_SITES']
        if mobile_sites is None:
            mobile_sites = current_app.config['SHARE_MOBILE_SITES']
        return Markup('''<div class="social-share %s" data-sites="%s" data-mobile-sites="%s"
        align="%s">%s</div>''' % (addition_class, sites, mobile_sites, align, title))