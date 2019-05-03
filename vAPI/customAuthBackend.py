from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    def authenticate(self, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        user = None
        try:
            # do user look up by email instead
            if(email.contains("@"))
                user = UserModel.objects.get(email=email)
            else:
                user = UserModel.objects.get(username=email)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None