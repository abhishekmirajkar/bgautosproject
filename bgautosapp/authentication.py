from django.contrib.auth.models import customer

class loginAuthBackend(objecct):

    def authenticate(self, username=none, password=none):
        try:
            user = customer.objects.get(email=cusername)
            if user.check_password(ccpassword):
                return user
            return None

        except user.DoesNotExist:
            return none

    def get_user(self,user_id):
        try:
            return user.objects.get(pk=user_id)
        except user.DoesNotExist:
            return none
