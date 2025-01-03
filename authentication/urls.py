from django.urls import path, include

from dj_rest_auth.registration.views import (
    ResendEmailVerificationView,
    VerifyEmailView,
)
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    UserDetailsView,
    PasswordResetConfirmView,
    PasswordResetView,
)

from authentication.views import (
    VerifyEmailCodeView
    # email_confirm_redirect,
    # password_reset_confirm_redirect,
)


urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('register/verify-email/', VerifyEmailCodeView.as_view(), name='verify_email_code'),
    path('register/', include('dj_rest_auth.registration.urls')),

    # path("register/", CustomRegisterView.as_view(), name="rest_register"),
    # path("login/", LoginView.as_view(), name="rest_login"),
    # path("logout/", LogoutView.as_view(), name="rest_logout"),
    # path("user/", UserDetailsView.as_view(), name="rest_user_details"),

    # path("register/verify-email/", VerifyEmailView.as_view(), name="rest_verify_email"),
    # path("register/resend-email/", ResendEmailVerificationView.as_view(), name="rest_resend_email"),
    # path("account-confirm-email/<str:key>/", email_confirm_redirect, name="account_confirm_email"),
    # path("account-confirm-email/", VerifyEmailView.as_view(), name="account_email_verification_sent"),
    # path("password/reset/", PasswordResetView.as_view(), name="rest_password_reset"),
    # path(
    #     "password/reset/confirm/<str:uidb64>/<str:token>/",
    #     password_reset_confirm_redirect,
    #     name="password_reset_confirm",
    # ),
    # path("password/reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]
