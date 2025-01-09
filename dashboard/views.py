from django.views.generic import TemplateView

from authentication.mixins import StaffRequiredMixin

class DashboardView(StaffRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'
