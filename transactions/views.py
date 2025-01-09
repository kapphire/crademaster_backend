from django.views.generic import ListView, DetailView

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from authentication.mixins import StaffRequiredMixin
from .models import Withdraw
from .serializers import WithdrawSerializer

class WithdrawCreateAPIView(generics.CreateAPIView):
    serializer_class = WithdrawSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class WithdrawListView(StaffRequiredMixin, ListView):
    model = Withdraw
    template_name = 'transactions/withdraw_list.html'
    context_object_name = 'withdraws'


class WithdrawDetailView(StaffRequiredMixin, DetailView):
    model = Withdraw
    template_name = 'transactions/withdraw_detail.html'
    context_object_name = 'withdraw'
