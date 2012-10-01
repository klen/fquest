from ..core.admin import admin
from .models import Character, Monster, Stuff, Event


admin.add_model(Character)
admin.add_model(Monster)
admin.add_model(Stuff)
admin.add_model(Event)
