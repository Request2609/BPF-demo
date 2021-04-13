from server import app

@app.route("/")
def index():
    print("hello world")
    return render_template('index.html')

@app.route('/request_info', methods=['POST', 'GET'])
def get_request_info():
    req_list = request.form.getlist("vehicle")
    async_process_request(pool, req_list)
    return "hello world"