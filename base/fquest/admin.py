from ..core.admin import admin
from .models import Character, Monster, Stuff


admin.add_model(Character)
admin.add_model(Monster)
admin.add_model(Stuff)
