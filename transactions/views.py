from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from authentication.mixins import StaffRequiredMixin
from .models import Withdraw
from .serializers import WithdrawSerializer, DepositSerializer


class WithdrawCreateAPIView(generics.CreateAPIView):
    serializer_class = WithdrawSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class DepositCreateAPIView(generics.CreateAPIView):
    serializer_class = DepositSerializer
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


class WithdrawDeleteView(StaffRequiredMixin, DeleteView):
    model = Withdraw
    template_name = 'transactions/withdraw_confirm_delete.html'
    success_url = reverse_lazy('withdraw_list')
