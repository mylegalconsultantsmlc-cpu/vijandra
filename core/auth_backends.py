from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class EmailOrMobileBackend(ModelBackend):
    """
    Authenticate using either email or mobile (stored in profiles).
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        identifier = username or kwargs.get('identifier')
        if not identifier:
            return None
        # try email first
        try:
            user = User.objects.get(email__iexact=identifier)
        except User.DoesNotExist:
            # try mobile in ClientProfile
            from .models import ClientProfile, AdvocateProfile
            client = ClientProfile.objects.filter(mobile=identifier).first()
            if client:
                user = client.user
            else:
                adv = AdvocateProfile.objects.filter(mobile=identifier).first()
                if adv:
                    user = adv.user
                else:
                    user = None
        if user and user.check_password(password):
            return user
        return None
