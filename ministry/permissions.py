from functools import wraps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

ADMIN_GROUP = 'Admins'
VIEWER_GROUP = 'Viewers'


def is_admin(user):
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return user.groups.filter(name=ADMIN_GROUP).exists()


def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        if not is_admin(request.user):
            messages.error(request, 'You do not have permission to perform that action. Viewers can read and download reports only.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped