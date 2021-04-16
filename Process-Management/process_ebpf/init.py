from flask import Flask
from markupsafe import escape
from application.view import init_view 


def init():
    app = Flask(__name__)
    init_view(app)
    return app 