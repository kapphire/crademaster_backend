from django.contrib import admin

from .models import Investment

class InvestmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'fee', 'created']
    list_filter = ['user', 'fee']
    search_fields = ['user__username', 'amount']
    list_editable = ['amount', 'fee']
    fields = ['user', 'amount', 'fee']

admin.site.register(Investment, InvestmentAdmin)
