from django.contrib import admin

from .models import Execute

class ExecuteAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'duration', 'created']
    list_filter = ['user', 'duration']
    search_fields = ['user__username', 'amount']
    fields = ['user', 'amount', 'duration', 'created']


admin.site.register(Execute, ExecuteAdmin)
