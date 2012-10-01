from flask_wtf import Form
from flaskext.babel import gettext as _
from wtforms.fields import TextField, SelectField, SubmitField

from . import config


class CharacterCreateForm(Form):

    race = SelectField(choices=config.RACE, coerce=int)
    sex = SelectField(choices=config.SEX, coerce=int)
    cls = SelectField(choices=config.CLASS, coerce=int, label=_('Character Class'))
    moto = TextField(_('Character moto'))

    create = SubmitField(_("Create"))
