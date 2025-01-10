from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from authentication.mixins import StaffRequiredMixin
from .models import Transaction
from .serializers import WithdrawSerializer


class WithdrawListView(StaffRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/withdraw_list.html'
    context_object_name = 'withdraws'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(transaction_type='WITHDRAWAL')


class WithdrawDetailView(StaffRequiredMixin, DetailView):
    model = Transaction
    template_name = 'transactions/withdraw_detail.html'
    context_object_name = 'withdraw'


class WithdrawDeleteView(StaffRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'transactions/withdraw_confirm_delete.html'
    success_url = reverse_lazy('withdraw_list')


# API views

class WithdrawCreateAPIView(generics.CreateAPIView):
    serializer_class = WithdrawSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
