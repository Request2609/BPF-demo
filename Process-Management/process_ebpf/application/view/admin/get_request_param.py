from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for
from flask_marshmallow import Marshmallow
from flask import request

req_proc_view = Blueprint('admin_index', __name__, url_prefix='/admin/')
ma = Marshmallow()

@req_proc_view.route("/get_req_param", methods =['GET', 'POST'])
def get_request_param():
    req_list = request.form.getlist("vehicle")
    get_list_type(req_list)
    prcoess_param_list()
    return "hello world"
