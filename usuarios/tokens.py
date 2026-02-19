from django.contrib.auth.tokens import PasswordResetTokenGenerator

class StablePasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # ignoramos last_login para evitar expiración inmediata
        return f"{user.pk}{user.password}{timestamp}"

password_reset_token = StablePasswordResetTokenGenerator()