from application.view.admin.get_request_param import req_proc_view

def init_admin_view(app):
    app.register_blueprint(req_proc_view)