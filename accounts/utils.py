# accounts/utils.py
from django.contrib.auth.models import User

def create_school_user(username, password, first_name, last_name, email="", is_staff=False):
    """Creates a new user account for students or staff members."""
    if User.objects.filter(username=username).exists():
        return None, "Username already exists."
    
    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email,
        is_staff=is_staff
    )
    return user, "Success"