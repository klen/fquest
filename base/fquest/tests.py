from ..core.tests import FlaskTest
from .generator import GEN_MONSTERS, GEN_STUFF


class TestCase(FlaskTest):

    def setUp(self):
        super(TestCase, self).setUp()

        # Create test world
        GEN_MONSTERS(num=100, max_level=20)
        GEN_STUFF(num=100, max_level=20)

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
