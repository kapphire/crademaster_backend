from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

from allauth.account.views import LoginView, LogoutView
from dj_rest_auth.registration.views import RegisterView

from .forms import CustomLoginForm
from .serializers import CustomRegisterSerializer


from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import EmailVerificationCode

User = get_user_model()

class VerifyEmailCodeView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        verification_code = request.data.get("verification_code")

        try:
            verification = EmailVerificationCode.objects.get(email=email, code=verification_code)
            
            if verification.is_expired:
                return JsonResponse({"error": "Verification code has expired"}, status=400)

            # You can now mark the email as verified in the EmailAddress model
            emailaddress = verification.emailaddress_set.first()  # Assuming the email address is linked to an EmailAddress object
            emailaddress.verified = True
            emailaddress.save()

            return JsonResponse({"success": "Email verified successfully!"}, status=200)

        except EmailVerificationCode.DoesNotExist:
            return JsonResponse({"error": "Invalid verification code"}, status=400)


# def email_confirm_redirect(request, key):
#     return HttpResponseRedirect(
#         f"{settings.EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/"
#     )


# def password_reset_confirm_redirect(request, uidb64, token):
#     return HttpResponseRedirect(
#         f"{settings.PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
#     )
