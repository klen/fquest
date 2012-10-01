from flask_mixer import Mixer

from . import config
from ..core.tests import FlaskTest
from .generator import GEN_MONSTERS, GEN_STUFF
from .models import Character, db, Event


class TestCase(FlaskTest):

    def setUp(self):
        super(TestCase, self).setUp()

        # Create test world
        GEN_MONSTERS(num=100, max_level=20)
        GEN_STUFF(num=100, max_level=20)

        self.mixer = Mixer(self.app)

    def test_monster(self):
        from .models import Monster
        from sqlalchemy import func

        monster = Monster.query.order_by(func.random()).first()
        self.assertTrue(monster)

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
