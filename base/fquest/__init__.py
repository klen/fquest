" base.fquest "


def loader_meta(app):
    " Init fquest stuff. "

    from .views import fquest
    app.register_blueprint(fquest)

    from .models import *

# pymode:lint_ignore=W404
