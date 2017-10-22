Flask-Share
===========

Create social share component in Jinja2 template based
on `share.js <https://github.com/overtrue/share.js/>`_.


Get Started
-----------

Installation is easy::

    $ pip install flask-share

Initialize the extension::

    from flask_share import Share
    ...
    share = Share(app)

Also support for factory pattern::

    from flask_share import Share
    share = Share()

    def create_app():
        app = Flask(__name__)
        ...
        share.init_app(app)


Example
-------

Here is a simple demo to demonstrate how to create a share component in
template::

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Flask-Share Demo</title>
        {{ share.load() }}
    </head>
    <body>
        <h1>Hello, Flask-Share!</h1>
	    <p>Maecenas tincidunt lacus at velit. Phasellus in felis. Praesent
	    id massa id nisl venenatis lacinia. Integer ac neque. Morbi ut odio.
	    Nullam varius. Sed vel enim sit amet nunc viverra dapibus. Nullam
	    varius. In hac habitasse platea dictumst.</p>
	    {{ share.create(title='Share with: ') }}
    </body>
    </html>

And here is what you get:

.. figure::  images/demo.png

  Before you ask, the share component is highly customizable.

Resources
---------

* `Documentation <None>`_
* `PyPI <None>`_

Development
-----------

We welcome all kinds of contributions. You can run test like this::

    $ python setup.py test

Authors
-------

Maintainer: `Grey Li <http://greyli.com>`_

See also the list of
`contributors <https://github.com/greyli/flask-share/contributors>`_
who participated in this project.

License
-------

This project is licensed under the MIT License (see the
``LICENSE`` file for details).
