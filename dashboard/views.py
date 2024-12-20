from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    # def dispatch(self, request, *args, **kwargs):
    #     # Check if the user is logged in and is a superuser
    #     if not request.user.is_superuser:
    #         messages.error(request, "You must be a superuser to access the dashboard.")
    #         return redirect(reverse('account_login'))
    #     return super().dispatch(request, *args, **kwargs)
