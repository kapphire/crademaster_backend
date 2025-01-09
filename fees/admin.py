from django.contrib import admin
from .models import Fee


class FeeAdmin(admin.ModelAdmin):
    list_display = ['min_investment', 'max_investment', 'fee_percentage', 'hours']
    list_filter = ['fee_percentage']
    search_fields = ['min_investment', 'max_investment', 'fee_percentage']
    ordering = ['min_investment']
    fields = ['min_investment', 'max_investment', 'fee_percentage', 'hours']


admin.site.register(Fee, FeeAdmin)
