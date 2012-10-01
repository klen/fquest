from ..ext import manager


@manager.command
def create_world():
    "Generate fquest world."

    from .generator import GEN_MONSTERS, GEN_STUFF

    GEN_MONSTERS(num=1000)
    GEN_STUFF(num=1000)


@manager.command
def give_exp(facebook_id, exp):
    " This is cheat. "
    from .models import Character, db

    character = Character.query.filter(Character.facebook_id == facebook_id).first()
    if character:
        character.got_exp(int(exp))

    db.session.commit()
