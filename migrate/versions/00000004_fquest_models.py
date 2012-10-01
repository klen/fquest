"""Added Key to auth

Revision ID: 00000004
Revises: 00000003
Create Date: 2012-10-01 20:54:46.332465

"""

# revision identifiers, used by Alembic.
revision = '00000004'
down_revision = '00000003'

from alembic import op
import sqlalchemy as db
from datetime import datetime


def upgrade():
    op.create_table(
        'fquest_character',

        db.Column('id', db.Integer, primary_key=True),
        db.Column('created_at', db.DateTime,
                  default=datetime.utcnow, nullable=False),
        db.Column('updated_at', db.DateTime,
                  onupdate=datetime.utcnow, default=datetime.utcnow),

        db.Column('name', db.String, nullable=False),
        db.Column('cls', db.SmallInteger, default=0, nullable=False),
        db.Column('race', db.SmallInteger, default=0, nullable=False),
        db.Column('sex', db.Boolean, default=True, nullable=False),
        db.Column('moto', db.String),

        db.Column('level', db.Integer, default=1, nullable=False),
        db.Column('health', db.Integer, default=20, nullable=False),
        db.Column('strenght', db.Integer, default=15, nullable=False),
        db.Column('dexterity', db.Integer, default=15, nullable=False),
        db.Column('intellect', db.Integer, default=15, nullable=False),
        db.Column('luck', db.Integer, default=15, nullable=False),

        db.Column('current_health', db.Integer, default=20, nullable=False),
        db.Column('alignment', db.SmallInteger, default=1, nullable=False),
        db.Column('gold', db.Integer, default=0, nullable=False),
        db.Column('death', db.Integer, default=0, nullable=False),
        db.Column('win', db.Integer, default=0, nullable=False),
        db.Column('lose', db.Integer, default=0, nullable=False),
        db.Column('exp', db.Integer, default=0, nullable=False),

        db.Column('guild_id', db.Integer, db.ForeignKey('fquest_guild.id')),
        db.Column('user_id', db.Integer, db.ForeignKey('auth_user.id'), nullable=False),
        db.Column('facebook_id', db.String, nullable=False),
        db.Column('facebook_token', db.String, nullable=False),
        db.Column('facebook_synced', db.DateTime, default=datetime.utcnow, nullable=False),
    )

    op.create_table(
        'fquest_monster',

        db.Column('id', db.Integer, primary_key=True),
        db.Column('created_at', db.DateTime,
                  default=datetime.utcnow, nullable=False),
        db.Column('updated_at', db.DateTime,
                  onupdate=datetime.utcnow, default=datetime.utcnow),

        db.Column('name', db.String, nullable=False, unique=True),
        db.Column('level', db.Integer, default=0, nullable=False),
        db.Column('race', db.Integer, default=7, nullable=False),
    )

    op.create_table(
        'fquest_stuff',

        db.Column('id', db.Integer, primary_key=True),
        db.Column('created_at', db.DateTime,
                  default=datetime.utcnow, nullable=False),
        db.Column('updated_at', db.DateTime,
                  onupdate=datetime.utcnow, default=datetime.utcnow),

        db.Column('name', db.String, nullable=False),
        db.Column('level', db.Integer, default=0, nullable=False),
        db.Column('mode', db.SmallInteger, default=0, nullable=False),
    )

    op.create_table(
        'fquest_guild',

        db.Column('id', db.Integer, primary_key=True),
        db.Column('created_at', db.DateTime,
                  default=datetime.utcnow, nullable=False),
        db.Column('updated_at', db.DateTime,
                  onupdate=datetime.utcnow, default=datetime.utcnow),

        db.Column('name', db.String, nullable=False),
    )

    op.create_table(
        'fquest_event',

        db.Column('id', db.Integer, primary_key=True),
        db.Column('created_at', db.DateTime,
                  default=datetime.utcnow, nullable=False),
        db.Column('updated_at', db.DateTime,
                  onupdate=datetime.utcnow, default=datetime.utcnow),

        db.Column('message', db.String, nullable=False),
        db.Column('gold', db.Integer, default=0, nullable=False),
        db.Column('exp', db.Integer, default=0, nullable=False),
        db.Column('level', db.Integer),

        db.Column('character_id', db.Integer, db.ForeignKey('fquest_character.id'), nullable=False),

        db.Column('facebook_id', db.String, unique=True),
        db.Column('facebook_created_time', db.String),
    )

    op.create_table(
        'fquest_achievement',

        db.Column('id', db.Integer, primary_key=True),
        db.Column('created_at', db.DateTime,
                  default=datetime.utcnow, nullable=False),
        db.Column('updated_at', db.DateTime,
                  onupdate=datetime.utcnow, default=datetime.utcnow),

        db.Column('type', db.SmallInteger, nullable=False),
        db.Column('name', db.String(50), nullable=False),
        db.Column('message', db.String(100), nullable=False),

        db.Column('character_id', db.Integer, db.ForeignKey('fquest_character.id'), nullable=False),
    )

    op.create_table(
        'fquest_inventory',

        db.Column('id', db.Integer, primary_key=True),
        db.Column('stuff_id', db.Integer, db.ForeignKey('fquest_stuff.id'), nullable=False),
        db.Column('character_id', db.Integer, db.ForeignKey('fquest_character.id'), nullable=False),
        db.Column('wearing', db.Boolean, default=False, nullable=False),
    )


def downgrade():
    op.drop_table('fquest_character')
    op.drop_table('fquest_monster')
    op.drop_table('fquest_stuff')
    op.drop_table('fquest_guild')
    op.drop_table('fquest_event')
    op.drop_table('fquest_achievement')
    op.drop_table('fquest_inventory')
