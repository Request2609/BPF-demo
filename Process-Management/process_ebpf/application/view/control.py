from server import app
from flask import Flask,request,make_response

@app.route("/")
def index():
    resp = make_response('set_cookie')
    resp.set_cookie('user_key', str(int(round(t * 1000000))))
    return render_template('index.html')

@app.route('/request_info', methods=['POST', 'GET'])
def get_request_info():
    req_list = request.form.getlist("vehicle")
    async_process_request(pool, req_list)
    return "hello world"