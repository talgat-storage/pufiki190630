from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.email) +
            six.text_type(user.password) +
            six.text_type(timestamp) +
            six.text_type(user.is_active)
        )


user_token_generator = TokenGenerator()
