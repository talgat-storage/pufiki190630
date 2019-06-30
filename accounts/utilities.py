from accounts.models import User


def get_existing_user(email, is_active):
    existing_user = None
    if email:
        existing_user = User.objects.all().filter(email=email, is_active=is_active).first()
    return existing_user
