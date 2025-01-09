from django.urls import path, include

from .views import DashboardView
from transactions.views import WithdrawListView, WithdrawDetailView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('fee/', include('fees.urls')),
    path('user/', include('users.urls')),
    path('withdraw/', WithdrawListView.as_view(), name="withdraw_list"),
    path('withdraw/<int:pk>/', WithdrawDetailView.as_view(), name="withdraw_detail"),
]
