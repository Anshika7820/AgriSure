from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/farmer/", views.register_farmer, name="register_farmer"),
    path("register/buyer/", views.register_buyer, name="register_buyer"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html",
            redirect_authenticated_user=True
        ),
        name="login"
    ),
    path("logout/", views.custom_logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/verify/", views.upload_verification, name="upload_verification"),

    # Password Change
    path(
        "password/change/",
        auth_views.PasswordChangeView.as_view(
            template_name="accounts/password_change.html",
            success_url="/dashboard/"
        ),
        name="password_change"
    ),

    # Fallback/aliases for standard Django accounts URLs
    path("accounts/login/", auth_views.LoginView.as_view(template_name="accounts/login.html", redirect_authenticated_user=True)),
    path("accounts/logout/", views.custom_logout),
    path("accounts/profile/", views.profile_view),
    path("accounts/register/farmer/", views.register_farmer),
    path("accounts/register/buyer/", views.register_buyer),
]
