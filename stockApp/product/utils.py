from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, product, timestamp):
        return text_type(product.is_active) + text_type(product.pk) + text_type(timestamp)


token_generator = AppTokenGenerator()