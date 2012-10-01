from __future__ import absolute_import

from celery import Celery
from celery.utils.log import get_task_logger
from flask import current_app as app

from ..app import create_app


logger = get_task_logger('fquest')


if not app:
    app = create_app()
    ctx = app.test_request_context()
    ctx.push()

celery = Celery('fquest')
celery.config_from_object(dict(
    BROKER_URL=app.config.get('BROKER_URL'),
    CELERYBEAT_SCHEDULE={
        'fquest-beat': {
            'task': 'base.fquest.celery.beat',
            'schedule': app.config.get('BEAT_SCHEDULE'),
        },
    }
))


@celery.task(ignore_result=True)
def beat():
    " FQuest beat. "

    from .models import Character
    character = Character.query.order_by(Character.facebook_synced.desc()).first()
    import ipdb; ipdb.set_trace() ### XXX BREAKPOINT


# pymode:lint_ignore=E061
