from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from django.contrib.auth.decorators import login_required

def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'teacher_profile'):
            messages.error(request, 'You must be a teacher to access this page')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'teacher_profile'):
            messages.error(request, 'You must be a teacher to access this page')
            return redirect('login')
        if not request.user.teacher_profile.is_admin:
            messages.error(request, 'You must be an admin to access this page')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def permission_required(permission):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not hasattr(request.user, 'teacher_profile'):
                messages.error(request, 'You must be a teacher to access this page')
                return redirect('login')
            if not request.user.has_perm(f'attendance.{permission}'):
                messages.error(request, f'You do not have permission to access this page')
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
