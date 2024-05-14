from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from store.models import user

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        User = get_user_model()

        try:
            print("----------Attempting to authenticate with email:", email)
            user_auth = User.objects.get(email=email)
            print("--User found:", user_auth)
            if user_auth.verify_password(password) and self.user_can_authenticate(user_auth):
                print("--Password verified successfully")
                return user_auth
            else:
                print("--Password verification failed")
        except User.DoesNotExist:
            print("--User not found")
        return None
