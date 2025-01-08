from django.http import JsonResponse

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .models import EmailVerificationCode


class VerifyEmailCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        verification_code = request.data.get("verification_code")

        try:
            verification = EmailVerificationCode.objects.get(email_address__email=email, code=verification_code)
            
            if verification.is_expired:
                return JsonResponse({"error": "Verification code has expired"}, status=400)

            # You can now mark the email as verified in the EmailAddress model
            emailaddress = verification.email_address
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
