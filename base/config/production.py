" Production settings must be here. "

from .core import *
from os import path as op
from datetime import timedelta


MODE = 'production'
SECRET_KEY = 'SecretKeyForSessionSigning'
ADMINS = MAIL_USERNAME and [MAIL_USERNAME] or None

# flask.ext.collect
# -----------------
COLLECT_STATIC_ROOT = op.join(op.dirname(ROOTDIR), 'static')

# dealer
DEALER_PARAMS = dict(
    backends=('git', 'mercurial', 'simple', 'null')
)

# FQUEST settings
# ---------------
AUTH_LOGIN_VIEW = 'fquest.index'
AUTH_PROFILE_VIEW = 'fquest.profile'
OAUTH_FACEBOOK = dict(
    consumer_key='365449256868307',
    consumer_secret='899b2ea26ca77122eef981f4712aeb04',
    params=dict(
        scope="user_status,user_likes,user_activities,user_questions,user_events,user_videos,user_groups,user_relationships,user_notes,user_photos,offline_access,publish_actions"
    )
)

# Cache
CACHE_TYPE = 'redis'
CACHE_REDIS_HOST = 'localhost'
CACHE_KEY_PREFIX = 'poliglot'

# Database settings
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://fquest:fquest@localhost:5432/fquest_master'

# Celery settings
BROKER_URL = 'redis://localhost:6379/2'
BEAT_SCHEDULE = timedelta(minutes=1)

if op.exists('/var/www/smtp'):
    with open('/var/www/smtp') as f:
        MAIL_USERNAME, MAIL_PASSWORD = f.read().strip().split(' ')
    ADMINS = [MAIL_USERNAME]

logging.info("Production settings loaded.")

# pymode:lint_ignore=W0614,W404
