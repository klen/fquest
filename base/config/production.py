" Production settings must be here. "

from .core import *
from os import path as op


SECRET_KEY = 'SecretKeyForSessionSigning'
ADMINS = frozenset([MAIL_USERNAME])

# flask.ext.collect
# -----------------
COLLECT_STATIC_ROOT = op.join(op.dirname(ROOTDIR), 'static')

# FQUEST settings
# ----------
AUTH_LOGIN_VIEW = 'fquest.index'
AUTH_PROFILE_VIEW = 'fquest.profile'
OAUTH_FACEBOOK = dict(
    consumer_key='365449256868307',
    consumer_secret='899b2ea26ca77122eef981f4712aeb04',
    params=dict(
        scope="user_status,user_likes,user_activities,user_questions,user_events,user_videos,user_groups,user_relationships,user_notes,user_photos,offline_access,publish_actions"
    )
)

# dealer
DEALER_PARAMS = dict(
    backends=('git', 'mercurial', 'simple', 'null')
)


# pymode:lint_ignore=W0614,W404
