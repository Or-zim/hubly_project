from django.test import TestCase
from users.models import User, AuthToken
from datetime import timedelta
from django.utils import timezone

class AuthTokenModelTest(TestCase):
    def test_new_token_is_valid(self):
        """We test that the newly created token is valid"""
        user = User.objects.create(
            username='ffff',
            first_name = 'number1',
            telegram_id = '1234567890')
        token = AuthToken.objects.create(user=user)
        result = token.is_valid()
        self.assertTrue(result)



    def test_expired_token_is_invalid(self):
        user = User.objects.create(username='number1', first_name='number1', telegram_id='1234567890')
        token = AuthToken.objects.create(user=user)
        token.created_at = timezone.now() - timedelta(minutes=5)
        token.save()
        result = token.is_valid()
        self.assertFalse(result)
