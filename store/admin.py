from django.contrib import admin
from .models import store

class storeAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        get_data = super(storeAdmin, self).get_changeform_initial_data(request)
        get_data['author'] = request.user
        return get_data

admin.site.register(store, storeAdmin)


