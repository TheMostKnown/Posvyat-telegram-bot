from django.contrib import admin

from .models import Organizers, Room, Guest, OrganizerSchedule, GuestSchedule, Level, Broadcast, Issue, Script, Button

admin.site.register(Organizers)
admin.site.register(Room)
admin.site.register(Guest)
admin.site.register(OrganizerSchedule)
admin.site.register(GuestSchedule)
admin.site.register(Level)
admin.site.register(Broadcast)
admin.site.register(Issue)
admin.site.register(Script)
admin.site.register(Button)
