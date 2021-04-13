from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for
from flask_marshmallow import Marshmallow

index_view = Blueprint('index', __name__, url_prefix='/')
ma = Marshmallow()

@index_view.route("/")
def index():
    return render_template('/index/index.html')
