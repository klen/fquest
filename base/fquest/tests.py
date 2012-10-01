from flask_mixer import Mixer

from . import config
from ..core.tests import FlaskTest
from .generator import GEN_MONSTERS, GEN_STUFF
from .models import Character, db, Event
from mock import Mock


class TestCase(FlaskTest):

    def setUp(self):
        super(TestCase, self).setUp()

        # Create test world
        GEN_MONSTERS(num=100, max_level=20)
        GEN_STUFF(num=100, max_level=20)

        self.mixer = Mixer(self.app, session_commit=True)

    def test_monster(self):
        from .models import Monster
        from sqlalchemy import func

        monster = Monster.query.order_by(func.random()).first()
        self.assertTrue(monster)

        character = self.mixer.blend(Character)

        monster = Monster.meet_character(character)
        self.assertTrue(abs(monster.level - character.level) <= 2)

        exp, gold = monster.get_stuff(character)
        self.assertTrue(exp is not None and gold is not None)

    def test_stuff(self):
        from .models import Stuff
        from sqlalchemy import func

        stuff = Stuff.query.order_by(func.random()).first()
        self.assertTrue(stuff)

    def test_character(self):
        character = self.mixer.blend(Character, sex=self.mixer.random, cls=config.CLASS_GEN)
        character.role()

        self.assertEqual(character.level, 1)
        self.assertEqual(character.health, 20)

        character.got_exp(150)
        self.assertEqual(character.level, 3)
        self.assertTrue(character.health >= 60)

        db.session.commit()
        event = character.events.order_by(Event.id.desc()).first()
        self.assertEqual(event.level, 3)

        for _ in xrange(70):
            Event.fight(character)

        db.session.commit()

        self.assertTrue(character.win)
        self.assertTrue(character.lose)
        self.assertTrue(character.gold)
        self.assertTrue(character.events.count() > 70)

    def test_beat(self):
        from .celery import beat
        from ..ext import cache
        from facepy import GraphAPI
        from sqlalchemy import func

        GraphAPI.get = Mock(return_value=dict(
            data=[
                dict(
                    id='1243',
                    type='status',
                    created_time="2012-10-01T07:45:59+0000",
                )
            ]
        ))

        cache.cache.clear()

        for _ in xrange(20):
            self.mixer.blend(Character)

        self.assertEqual(Event.query.count(), 0)

        beat()
        last_update1 = cache.get('fquest.last_synced')

        GraphAPI.get = Mock(return_value=dict(
            data=[
                dict(
                    id='124356',
                    type='status',
                    created_time="2012-10-01T07:45:59+0000",
                )
            ]
        ))
        beat()

        last_update2 = cache.get('fquest.last_synced')
        self.assertEqual(Event.query.count(), 11)
        self.assertTrue(last_update2 > last_update1)

        character = Character.query.order_by(Character.facebook_synced.desc()).first()
        self.assertTrue(character.facebook_synced > last_update2)
