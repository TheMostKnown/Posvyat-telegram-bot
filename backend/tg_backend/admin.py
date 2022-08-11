from django.contrib import admin

from .models import organizers, room, guest, organizer_schedule, guest_schedule, level, broadcast, issue, script, button


admin.site.register(organizers)
admin.site.register(room)
admin.site.register(guest)
admin.site.register(organizer_schedule)
admin.site.register(guest_schedule)
admin.site.register(level)
admin.site.register(broadcast)
admin.site.register(issue)
admin.site.register(script)
admin.site.register(button)
