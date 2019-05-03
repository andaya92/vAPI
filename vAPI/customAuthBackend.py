from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    def authenticate(self, email=None, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        user = None
        print(email, username)
        try:
        # do user look up by email instead
            if username:
                user = UserModel.objects.get(username=username)
            elif email:
                user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            return None
        if user:
            print(user)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None