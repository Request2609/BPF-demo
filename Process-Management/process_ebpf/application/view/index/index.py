from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for,make_response
from flask_marshmallow import Marshmallow
import time
import datetime

index_view = Blueprint('index', __name__, url_prefix='/')
ma = Marshmallow()


@index_view.route("/")
def index():
    return render_template('/index/index.html')

def get_cookie():
    cookie_value = request.cookies.get('user_key')