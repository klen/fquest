# Monster and Stuff generator
from itertools import product
from random import randrange, randint
from .models import Monster, db, Stuff
from sqlalchemy.exc import IntegrityError, DataError
from flask import current_app

MONSTER_NAMES = (
    ('Bear', 'Boar', 'Cougar', 'Cat', 'Devilsaurs', 'Dragonhawk', 'Gryphon', 'Raptor', 'Spider', 'Wolve'),
    ('Archimonde', 'Kiljaeden', 'Tichondrius', 'Mannoroth', 'Kazzak', 'Xavius', 'Sayaad', 'Imp', 'Satyr', 'Terror'),
    ('Wyrm', 'Dragon', 'Drake', 'Whelp', 'Drakonid', 'Aspect'),
    ('Air Elemental', 'Earth Elemental', 'Fire Elemental', 'Water Elemental', 'Ice Elemental', 'Lava Elemental'),
    ('Gron', 'Ogr', 'Magnataur', 'Vrykul', 'Colossi', 'Giant'),
    ('Gnome', 'Goblin', 'Kobold', 'Dwarf', 'Trogg', 'Gnoll', 'Orc', 'Harpy', 'Naga'),
    ('Shredder', 'Golem', 'Bombling', 'Alarm-O-Bot', 'Mechagnome'),
    ('Banshee', 'Ghost', 'Lich', 'Zombie', 'Mummy'),
)

ADJECTIVIES = (
    '', 'Hyngry', 'Fat', 'Crazy', 'Angry', 'Serious', 'Strong', 'Evil', 'Small', 'Older', 'Awful'
)

COLORS = (
    '', 'Red', 'Black', 'Green', 'Yellow', 'Blue', 'White'
)

STUFF_ADJ = 'Tigger', 'Crane', 'Guardian', "Firebird's", 'Dreadwoven', 'Gold', 'Silver'

STUFF_NAMES = (
    ('Skull', 'Headguard', 'Helm', 'Crown', 'Helmet', 'Cover'),
    ('Necklace', 'Shackle', 'Amulet', 'Pendant', 'Beads', 'Cachabon'),
    ('Mantle', 'Pauldrons', 'Shoulders', 'Shoulderguards', 'Blades', 'Spaulders'),
    ('Robes', 'Tunic', 'Vest', 'Chestguard', 'Battleplate', 'Breastplate'),
    ('Armbands', 'Bracers', 'Cuffs', 'Wristbands', 'Wristguards', 'Armguards'),
    ('Dagger', 'Sword', 'Bow', 'Gun', 'Stave', 'Wand'),
    ('Gauntlets', 'Gloves', 'Glutches', 'Grips', 'Claws', 'Handguards'),
    ('Waistplate', 'Belt', 'Cord', 'Chain', 'Girdle', 'Fetters'),
    ('Legguards', 'Leggings', 'Legplates', 'Legwraps', 'Kilt', 'Greaves'),
    ('Ring', 'Signet', 'Band', 'Seal', 'Circle', 'Circuit'),
    ('Boots', 'Sandals', 'Greatboots', 'Stompers', 'Sollerets', 'Worldwalkers'),
)


def GEN_MONSTERS(num=600, max_level=100):

    monster_soup = list(product(
        xrange(len(COLORS)),
        xrange(len(ADJECTIVIES)),
        xrange(len(MONSTER_NAMES)),
        xrange(4),
    ))
    while num:
        color, adj, race, name = monster_soup.pop(randrange(len(monster_soup)))
        name = " ".join((
            COLORS[color],
            ADJECTIVIES[adj],
            MONSTER_NAMES[race][name]
        )).replace('  ', ' ').strip()
        level = randint(1, 100)
        monster = Monster(level=level, race=race, name=name)
        num -= 1

        try:
            db.session.add(monster)
            db.session.commit()
            current_app.logger.debug(str(monster))
        except (IntegrityError, DataError):
            db.session.rollback()


def GEN_STUFF(num=600, max_level=100):
    stuff_soup = list(product(
        xrange(len(COLORS)),
        xrange(len(STUFF_ADJ)),
        xrange(len(STUFF_NAMES)),
        xrange(5),
    ))
    while num:
        color, adj, mode, name = stuff_soup.pop(randrange(len(stuff_soup)))
        name = " ".join((
            COLORS[color],
            STUFF_ADJ[adj],
            STUFF_NAMES[mode][name]
        )).replace('  ', ' ').strip()
        level = randint(1, 100)
        stuff = Stuff(level=level, mode=mode, name=name)
        num -= 1

        try:
            db.session.add(stuff)
            db.session.commit()
            current_app.logger.debug(str(stuff))
        except (IntegrityError, DataError):
            db.session.rollback()
