from ..ext import manager


@manager.command
def create_world():
    "Generate fquest world."

    from .generator import GEN_MONSTERS, GEN_STUFF

    GEN_MONSTERS(num=1000)
    GEN_STUFF(num=1000)
