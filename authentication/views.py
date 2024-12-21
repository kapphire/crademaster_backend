from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from allauth.account.views import LoginView
from dj_rest_auth.registration.views import RegisterView

from .forms import CustomLoginForm
from .serializers import CustomRegisterSerializer


def email_confirm_redirect(request, key):
    return HttpResponseRedirect(
        f"{settings.EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/"
    )


def password_reset_confirm_redirect(request, uidb64, token):
    return HttpResponseRedirect(
        f"{settings.PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
    )

class CustomRegisterView(RegisterView):
    serializer_class=CustomRegisterSerializer


class CustomLoginView(LoginView):
    form_class = CustomLoginForm

    def get_success_url(self):
        return settings.LOGIN_REDIRECT_URL


class PlaceholderView(TemplateView):
    template_name = "account/placeholder.html"
