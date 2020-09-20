from django.contrib import admin
from .models import events,registered_to_event, Gallery

class eventsAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        get_data = super(eventsAdmin, self).get_changeform_initial_data(request)
        get_data['author'] = request.user
        return get_data

admin.site.register(events, eventsAdmin)
admin.site.register(registered_to_event)
admin.site.register(Gallery, eventsAdmin)
