from django.views.generic.list import ListView

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from authentication.mixins import StaffRequiredMixin
from authentication.serializers import CustomUserSerializer

from .models import CustomUser


class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserListView(StaffRequiredMixin, ListView):
    model = CustomUser
    template_name = 'users/list.html'
    context_object_name = 'users'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.exclude(is_staff=True)
