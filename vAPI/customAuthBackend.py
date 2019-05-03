from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    def authenticate(self, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        user = None
        print(email)
        # try:
        # do user look up by email instead
        if "@" in email:
            user = UserModel.objects.filter(email=email)
        else:
            user = UserModel.objects.filter(username=email)
        # except UserModel.DoesNotExist:
        #     return None
        if user:
            if user[0].check_password(password) and self.user_can_authenticate(user[0]):
                return user
        return None