from flaskext.babel import gettext as _
from random import randint, choice


LEVELS = dict(
    enumerate([100, 142, 201, 286, 406, 577, 819, 1164, 1653, 2347, 3333, 4733, 6721, 9544, 13553, 19245, 27328, 38806, 55104, 78248, 111113, 157781, 224049, 318149, 451772, 641517, 910955, 1293556, 1836849, 2608326, 3703823, 5259429, 7468390, 10605114, 15059262, 21384153, 30365497, 43119006, 61228988, 86945163, 123462132, 175316228, 248949044, 353507643, 501980853, 712812812, 1012194193, 1437315754, 2040988371], 1))

RACE = (
    (0, _("Human")),
    (1, _("Dwarf")),
    (2, _("Night Elf")),
    (3, _("Gnome")),
    (4, _("Draenel")),
    (5, _("Worgen")),
    (6, _("Pandaren")),
    (7, _("Orc")),
    (8, _("Undead")),
    (9, _("Tauren")),
    (10, _("Troll")),
    (11, _("Blood elf")),
    (12, _("Goblin")),
)
RACE_DISPLAY = dict(RACE)
RACE_GEN = lambda: randint(0, len(RACE) - 1)


SEX = (
    (0, _("Female")),
    (1, _("Male")),
)
SEX_DISPLAY = dict(SEX)

CLASS = (
    (0, _("Death Knight")),
    (1, _("Druid")),
    (2, _("Hunter")),
    (3, _("Mage")),
    (4, _("Paladin")),
    (5, _("Priest")),
    (6, _("Rogue")),
    (7, _("Shaman")),
    (8, _("Warlock")),
    (9, _("Warrior")),
)
CLASS_DISPLAY = dict(CLASS)
CLASS_GEN = lambda: randint(0, len(CLASS) - 1)
# Strenght, Dexterity, Intellect, Luck
CLASS_FABRIC = (
    (20, 15, 10, 15),  # Knight
    (15, 10, 20, 15),  # Druid
    (15, 25, 10, 10),  # Hunter
    (10, 10, 25, 15),  # Mage
    (15, 15, 15, 15),  # Paladin
    (15, 10, 20, 15),  # Priest
    (10, 20, 15, 15),  # Rogue
    (15, 10, 20, 15),  # Shaman
    (15, 10, 20, 15),  # Warlock
    (25, 15, 10, 10),  # Knight
)
CLASS_FABRIC_GEN = map(
    lambda x: map(
        lambda s: (lambda: randint(s - 2, s + 2)),
        x
    ),
    CLASS_FABRIC
)

MONSTER_RACE = (
    (0, _("Beast")),
    (1, _("Demon")),
    (2, _("Dragonkin")),
    (3, _("Elemental")),
    (4, _("Giant")),
    (5, _("Humanoid")),
    (6, _("Mechanical")),
    (7, _("Undead")),
)
MONSTER_RACE_DISPLAY = dict(MONSTER_RACE)
MONSTER_RACE_GEN = lambda: randint(0, len(MONSTER_RACE) - 1)

STUFF_MODE = (
    (0, _("Helm")),
    (1, _("Necklace")),
    (2, _("Shoulder")),
    (3, _("Chest")),
    (4, _("Wrist")),
    (5, _("Weapon")),
    (6, _("Hands")),
    (7, _("Waist")),
    (8, _("Legs")),
    (9, _("Ring")),
    (10, _("Boots")),
)
STUFF_MODE_DISPLAY = dict(STUFF_MODE)
STUFF_MODE_GEN = lambda: randint(0, len(STUFF_MODE) - 1)

EVENT_MODE = (
    (0, _('Fight')),
    (1, _('Search')),
)

WIN_PHRASE = (
    '%(target)s was massacred by %(character)s',
    '%(character)s broke %(target)s completely',
    '%(character)s easily defeated %(target)s',
    '%(character)s won a battle vs %(target)s',
)
WIN_PHRASE_GEN = lambda: choice(WIN_PHRASE)

LOSE_PHRASE = (
    '%(character)s was defeated by %(target)s',
    '%(character)s was hit by %(target)s',
    '%(character)s was completely broken by %(target)s',
)
LOSE_PHRASE_GEN = lambda: choice(LOSE_PHRASE)

ESCAPE_PHRASE = (
    '%(character)s could not kill %(target)s and escaped',
    '%(character)s avoided death by %(target)s',
    'Hero met %(target)s but not kill it',
)
ESCAPE_PHRASE_GEN = lambda: choice(ESCAPE_PHRASE)

LEVEL_PHRASE = (
    'Congratulations! %(character)s raised his level to %(level)s',
    '%(character)s is %(level)s level now!',
)
LEVEL_PHRASE_GEN = lambda: choice(LEVEL_PHRASE)
