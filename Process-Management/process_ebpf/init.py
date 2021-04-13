from flask import Flask
from markupsafe import escape
from application.view import init_view 

# 自定义信号处理函数
def my_handler(signum, frame):
    global stop
    stop = True
    pool.shutdown()
    

# 设置相应信号处理的handler
signal.signal(signal.SIGINT, my_handler)
signal.signal(signal.SIGHUP, my_handler)
signal.signal(signal.SIGTERM, my_handler)

def init():
    app = Flask(__name__)
    init_view(app)
    return app 