from django.contrib import admin

from .models import Fee, Investment

class InvestmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'fee', 'created']
    list_filter = ['user', 'fee']
    search_fields = ['user__username', 'amount']
    list_editable = ['amount', 'fee']
    fields = ['user', 'amount', 'fee']


class FeeAdmin(admin.ModelAdmin):
    list_display = ['min_investment', 'max_investment', 'fee_percentage']
    list_filter = ['fee_percentage']
    search_fields = ['min_investment', 'max_investment', 'fee_percentage']
    ordering = ['min_investment']
    fields = ['min_investment', 'max_investment', 'fee_percentage']


admin.site.register(Fee, FeeAdmin)
admin.site.register(Investment, InvestmentAdmin)
