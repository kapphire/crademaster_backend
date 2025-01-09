from django.views.generic.list import ListView

from authentication.mixins import StaffRequiredMixin
from .models import CustomUser

class UserListView(StaffRequiredMixin, ListView):
    model = CustomUser
    template_name = 'users/list.html'
    context_object_name = 'users'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.exclude(is_staff=True)
