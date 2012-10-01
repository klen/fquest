" base.fquest "


def loader_meta(app):
    from .views import fquest
    app.register_blueprint(fquest)
