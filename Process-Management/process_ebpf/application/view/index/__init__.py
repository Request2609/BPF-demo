from application.view.index.index import index_view

def init_index_view(app) :
    app.register_blueprint(index_view)