from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def farmer_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if not request.user.is_farmer():
            messages.error(request, "Access restricted: This area is only available to registered Farmers.")
            return redirect("dashboard")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def buyer_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if not request.user.is_buyer():
            messages.error(request, "Access restricted: This area is only available to registered Buyers.")
            return redirect("dashboard")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if not (request.user.is_platform_admin() or request.user.is_superuser):
            messages.error(request, "Access restricted: Administrator credentials required.")
            return redirect("dashboard")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
