from django.shortcuts import redirect
from functools import wraps
from .models import Profile

def admin_only(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        # 🔐 Check login
        if not request.user.is_authenticated:
            return redirect("login")

        # 🔥 Get profile safely
        profile, created = Profile.objects.get_or_create(user=request.user)

        # 🔐 Role check
        if profile.role.lower() != "admin":
            return redirect("dashboard")

        return view_func(request, *args, **kwargs)

    return wrapper