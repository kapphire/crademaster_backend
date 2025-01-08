from django.views.generic.list import ListView

from .models import CustomUser

class UserListView(ListView):
    model = CustomUser
    template_name = 'users/list.html'  # Optional: Custom template name
    context_object_name = 'users'
