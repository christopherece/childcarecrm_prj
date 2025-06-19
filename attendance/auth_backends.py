from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import Teacher

User = get_user_model()

class TeacherBackend(ModelBackend):
    """Custom authentication backend for teachers"""
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                # Check if user has a teacher profile
                if hasattr(user, 'teacher_profile'):
                    return user
        except User.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            # Only return user if they have a teacher profile
            if hasattr(user, 'teacher_profile'):
                return user
            return None
        except User.DoesNotExist:
            return None
