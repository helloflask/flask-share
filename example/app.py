# -*- coding: utf-8 -*-
from flask import Flask, render_template

from flask_share import Share

app = Flask(__name__)
share = Share(app)


@app.route('/')
def index():
    return render_template('index.html')
