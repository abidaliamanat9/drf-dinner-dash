from django.urls import path
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView, ResendEmailVerificationView
from dj_rest_auth.views import LoginView, LogoutView, UserDetailsView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from authentication.views import email_confirm_redirect, password_reset_confirm_redirect

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user/", UserDetailsView.as_view(), name="user_details"),
    path("register/verify-email/", VerifyEmailView.as_view(), name="register_verify_email"),
    path("register/resend-email/", ResendEmailVerificationView.as_view(), name="register_resend_email"),
    path("account-confirm-email/<str:key>/", email_confirm_redirect, name="account_confirm_email"),
    path("password/reset/", PasswordResetView.as_view(), name="password_reset"),
    path(
        "password/reset/confirm/<str:uidb64>/<str:token>/",
        password_reset_confirm_redirect,
        name="password_reset_confirm_frontend",
    ),
    path("password/reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password/change/", PasswordChangeView.as_view(), name="password_change")
]

