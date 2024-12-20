from django.urls import path
from .views import InvestmentListCreateAPIView

urlpatterns = [
    path('', InvestmentListCreateAPIView.as_view(), name='investment-list-create'),
]
