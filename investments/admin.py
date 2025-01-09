from django.contrib import admin

from .models import Investment, Usage

class InvestmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'fee', 'created']
    list_filter = ['user', 'fee']
    search_fields = ['user__username', 'amount']
    fields = ['user', 'amount', 'fee']


class UsageAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'duration', 'created']
    list_filter = ['user', 'duration']
    search_fields = ['user__username', 'amount']
    fields = ['user', 'amount', 'duration', 'created']


admin.site.register(Investment, InvestmentAdmin)
admin.site.register(Usage, UsageAdmin)
