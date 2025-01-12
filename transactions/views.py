from django.views.generic import (
    ListView, DetailView, DeleteView, UpdateView
)
from django.urls import reverse_lazy
from django.utils import timezone

from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from authentication.mixins import StaffRequiredMixin
from .models import Transaction
from .serializers import DepositSerializer, WithdrawSerializer
from .handler import trx_transfer_usdt


class DepositListView(StaffRequiredMixin, ListView):
    model = Transaction
    template_name = 'transactions/deposit_list.html'
    context_object_name = 'deposits'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(transaction_type='DEPOSIT')
    

class DepositDetailView(StaffRequiredMixin, DetailView):
    model = Transaction
    template_name = 'transactions/deposit_detail.html'
    context_object_name = 'deposit'


class DepositApproveView(StaffRequiredMixin, UpdateView):
    model = Transaction
    fields = []
    template_name = 'transactions/deposit_approve.html'
    context_object_name = 'deposit'
    success_url = reverse_lazy('deposit_list')

    def get_object(self):
        return Transaction.objects.get(id=self.kwargs['pk'])

    def form_valid(self, form):
        instance = form.save(commit=False)
        try:
            tx = trx_transfer_usdt(
                instance.user.cm_wallet,
                instance.user.cm_private_key,
                self.request.user.cm_wallet,
                instance.amount
            )
            instance.completed_at = timezone.now()
            instance.status = 'COMPLETED'
            instance.description = tx.get('result')
        except Exception as e:
            instance.completed_at = timezone.now()
            instance.status = 'FAILED'
            instance.description = e
        instance.save()

        return super().form_valid(form)


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

# class DepositCreateAPIView(generics.CreateAPIView):
#     serializer_class = DepositSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         try:
#             user = self.request.user
#             trx_transfer_usdt()
#             serializer.save(user=user, transaction_type='Deposit')
#         except Exception as e:
#             raise ValidationError(f"Transaction failed: {str(e)}")


class WithdrawCreateAPIView(generics.CreateAPIView):
    serializer_class = WithdrawSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user, transaction_type='WITHDRAWAL')
