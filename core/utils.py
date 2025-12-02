from django.contrib.auth import get_user_model
import random
import string

def generate_unique_username():
    """Generate a random username to avoid duplicates."""
    length = 8  # Length of the random string
    User = get_user_model()  # This ensures we use the custom User model
    while True:
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        if not User.objects.filter(username=username).exists():  # Check if username exists
            return username
