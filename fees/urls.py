from django.urls import path
from .views import FeeListView, FeeUpdateView

urlpatterns = [
    path('', FeeListView.as_view(), name='fee_list'),
    path('<int:pk>/edit/', FeeUpdateView.as_view(), name='fee_update'),
]
