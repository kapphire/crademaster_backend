"""
URL configuration for crademaster project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView, TemplateView

from allauth.account.views import LoginView, LogoutView

from investments.views import UsageCreateAPIView
from transactions.views import WithdrawCreateAPIView, DepositCreateAPIView
from users.views import UserDetailAPIView


urlpatterns = [
    path('', RedirectView.as_view(url='dashboard', permanent=False)),
    path('auth/', include('authentication.urls')),
    path('api/user-details/', UserDetailAPIView.as_view(), name='user_details'),
    path('api/activate/', UsageCreateAPIView.as_view(), name='usage_create'),
    path('api/withdraw/', WithdrawCreateAPIView.as_view(), name='withdraw_create'),
    path('api/deposit/', DepositCreateAPIView.as_view(), name='deposit_create'),

    path('accounts/login/', LoginView.as_view(), name='account_login'),
    path('accounts/signup/', TemplateView.as_view(), name="account_signup"),
    path('accounts/logout/', LogoutView.as_view(), name="account_logout"),

    path('investments/', include('investments.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('admin/', admin.site.urls),
]
