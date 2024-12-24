from django.contrib import admin

from .models import EmailVerificationCode

@admin.register(EmailVerificationCode)
class EmailVerificationCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'code', 'created_at')
    search_fields = ('email', 'code', 'user__username', 'user__email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
