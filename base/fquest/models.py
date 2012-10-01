from sqlalchemy.ext.declarative import declared_attr

from . import config
from ..core.models import BaseMixin, db, datetime


class Inventory(db.Model):

    __tablename__ = 'fquest_inventory'

    id = db.Column(db.Integer, primary_key=True)
    stuff_id = db.Column(db.Integer, db.ForeignKey('fquest_stuff.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('fquest_character.id'), nullable=False)
    wearing = db.Column(db.Boolean, default=False, nullable=False)


class Achievement(db.Model, BaseMixin):

    __tablename__ = 'fquest_achievement'
    __table_args__ = db.UniqueConstraint('character_id', 'type'),

    type = db.Column(db.SmallInteger, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(100), nullable=False)

    character_id = db.Column(db.Integer, db.ForeignKey('fquest_character.id'), nullable=False)
    character = db.relation('Character', lazy='joined', backref=db.backref(
        'achievements', lazy='subquery'))

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<Achievement "%s">' % (self.name)


class Character(db.Model, BaseMixin):

    __tablename__ = 'fquest_character'

    name = db.Column(db.String, nullable=False)
    cls = db.Column(db.SmallInteger, default=0, nullable=False)
    race = db.Column(db.SmallInteger, default=0, nullable=False)
    sex = db.Column(db.Boolean, default=True, nullable=False)
    moto = db.Column(db.String)

    level = db.Column(db.Integer, default=1, nullable=False)
    health = db.Column(db.Integer, default=20, nullable=False)
    strenght = db.Column(db.Integer, default=15, nullable=False)
    dexterity = db.Column(db.Integer, default=15, nullable=False)
    intellect = db.Column(db.Integer, default=15, nullable=False)
    luck = db.Column(db.Integer, default=15, nullable=False)

    current_health = db.Column(db.Integer, default=20, nullable=False)
    alignment = db.Column(db.SmallInteger, default=1, nullable=False)
    gold = db.Column(db.Integer, default=0, nullable=False)
    death = db.Column(db.Integer, default=0, nullable=False)
    win = db.Column(db.Integer, default=0, nullable=False)
    lose = db.Column(db.Integer, default=0, nullable=False)
    exp = db.Column(db.Integer, default=0, nullable=False)

    guild_id = db.Column(db.Integer, db.ForeignKey('fquest_guild.id'))
    guild = db.relationship('Guild', backref=db.backref('characters', lazy='dynamic'))

    user_id = db.Column(db.Integer, db.ForeignKey('auth_user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('characters', lazy='dynamic'))

    facebook_id = db.Column(db.String, nullable=False)
    facebook_synced = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<Character "%s" [%s]>' % (self.name, self.level)

    @declared_attr
    def inventory(self):
        assert self
        return db.relationship("Stuff", secondary='fquest_inventory', backref="characters")

    def role(self):
        assert [self.strenght, self.dexterity, self.intellect, self.luck] == [15, 15, 15, 15]
        gen = config.CLASS_FABRIC_GEN[self.cls]
        self.strenght, self.dexterity, self.intellect, self.luck = map(lambda x: x(), gen)


class Monster(db.Model, BaseMixin):

    __tablename__ = 'fquest_monster'

    name = db.Column(db.String, nullable=False, unique=True)
    level = db.Column(db.Integer, default=0, nullable=False)
    race = db.Column(db.Integer, default=7, nullable=False)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<Monster "%s" [%s]>' % (self.name, self.level)


class Stuff(db.Model, BaseMixin):

    __tablename__ = 'fquest_stuff'

    name = db.Column(db.String, nullable=False)
    level = db.Column(db.Integer, default=0, nullable=False)
    mode = db.Column(db.SmallInteger, default=0, nullable=False)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<Stuff "%s" [%s]>' % (self.name, self.level)


class Guild(db.Model, BaseMixin):

    __tablename__ = 'fquest_guild'

    name = db.Column(db.String, nullable=False)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<Guild "%s">' % self.name


class Event(db.Model, BaseMixin):

    __tablename__ = 'fquest_event'

    message = db.Column(db.String, nullable=False)
    gold = db.Column(db.Integer, default=0, nullable=False)
    exp = db.Column(db.Integer, default=0, nullable=False)
    level = db.Column(db.Integer)

    character_id = db.Column(db.Integer, db.ForeignKey('fquest_character.id'), nullable=False)
    character = db.relationship('Character', backref=db.backref('events', lazy='dynamic'))

    facebook_id = db.Column(db.String, unique=True)
    facebook_created_time = db.Column(db.String)

    def __unicode__(self):
        return self.message

    def __repr__(self):
        return '<Event "%s">' % self.message
