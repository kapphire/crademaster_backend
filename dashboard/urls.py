from allauth.account.views import logout
from authentication.views import CustomLoginView, PlaceholderView

from django.urls import path
from .views import DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('accounts/login/', CustomLoginView.as_view(), name='account_login'),
    path('accounts/signup/', PlaceholderView.as_view(), name="account_signup"),
    path('logout/', logout, name="account_logout"),
]
