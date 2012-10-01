from __future__ import absolute_import

from datetime import datetime

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
    " Fetch character progress. "

    from .models import Character, db, Event
    from ..ext import cache
    from facepy import GraphAPI, FacepyError

    last_synced = cache.get('fquest.last_synced')
    logger.info('BEAT')

    if last_synced:
        characters = Character.query.filter(Character.facebook_synced <= last_synced).limit(10)

    else:
        characters = [Character.query.order_by(Character.facebook_synced.desc()).first()]

    cache.set('fquest.last_synced', datetime.now(), timeout=300)

    for character in characters:
        Event.fire(character)

    db.session.commit()


@celery.task
def publish(token, ignore_result=True):
    " Async action publush. "
    from facepy import GraphAPI, FacepyError
    graph = GraphAPI(token)
    graph.post('/me/)


# pymode:lint_ignore=E061
