import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from model_bakery import baker

User = get_user_model()


class RegisterTestCase(TestCase):
    def test_register_user_success(self):
        response = self.client.post(reverse('register_user'), json.dumps({
            'username': 'test_user',
            'password': 'ljaskdjhfljah7384DKSLJFH&#$',
            'password2': 'ljaskdjhfljah7384DKSLJFH&#$',
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username='test_user').exists())

    def test_register_wrong_second_password_failure(self):
        response = self.client.post(reverse('register_user'), json.dumps({
            'username': 'test_user2',
            'password': 'ljaskdjhfljah7384DKSLJFH&#$',
            'password2': 'ljaskdjhfljah7384DKS&#$',
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(username='test_user2').exists())

    def test_register_duplicate_user_failure(self):
        fake_user = baker.make('auth.User')
        response = self.client.post(reverse('register_user'), json.dumps({
            'username': fake_user.username,
            'password': 'ljaskdjhfljah7384DKSLJFH&#$',
            'password2': 'ljaskdjhfljah7384DKSLJFH&#$',
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['username'][0].code, 'unique')
