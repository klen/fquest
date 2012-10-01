from __future__ import absolute_import
import time
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

    cache.set('fquest.last_synced', datetime.now())

    for character in characters:
        graph = GraphAPI(oauth_token=character.facebook_token)

        # Create timestamp since
        since = int(time.mktime(character.facebook_synced.timetuple()))
        uri = '/me/feed?fields=type,name&since=%s' % since

        try:
            logger.info('Call API: %s' % uri)
            feed = graph.get(uri)
            assert 'data' in feed and feed['data']
        except (FacepyError, AssertionError), e:
            logger.error(e)

        for info in feed['data']:
            Event.fight(character)

        character.facebook_synced = datetime.now()

    db.session.commit()


# pymode:lint_ignore=E061
