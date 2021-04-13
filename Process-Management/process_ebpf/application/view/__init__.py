from application.view.index import init_index_view
from application.view.admin import init_admin_view

def init_view(app):
    init_index_view(app)
    init_admin_view(app)