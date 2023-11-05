import json
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import tag, modify_settings
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APITestCase

# Create your tests here.
from users.serializers import text_words_count

User = get_user_model()


def mock_fetch_from_datasource(text):
    print('mock fetch called')
    return 6


class ProfileTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(username="test")
        self.random_users = baker.make_recipe('users.user_recipe', _quantity=5)
        self.user.set_password("test")
        self.user.save()

    @tag("success")
    def test_words_count_success(self):
        result = text_words_count("sample text")
        self.assertEqual(result, 2)

    @tag("failure")
    def test_words_count_wrong_input(self):
        with self.assertRaises(ValueError):
            text_words_count(None)

    def test_get_profile_unauthorized(self):
        result = self.client.get("/users/profile")
        self.assertEqual(result.status_code, 401)

    @patch('users.serializers.fetch_from_data_source')
    def test_get_profile_success(self, mock_fetch):
        mock_fetch.return_value = 7
        # mock_fetch.side_effect = Exception("unknown error")
        login_result = self.client.post(reverse("token_obtain_pair"), json.dumps(
            {
                "username": "test",
                "password": "test"
            }
        ), content_type="application/json")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_result.data.get('access')}")
        result = self.client.get("/users/profile")
        self.assertEqual(result.status_code, 200)
        self.assertIsNone(result.data.get("full_name"))
        self.assertEqual(result.data.get("name_words"), 5)

    @patch('requests.get')
    def test_get_profile_with_cache_success(self, mock_get):
        print(self.random_users[3].__dict__)
        mock_get.return_value = 8
        with modify_settings(MIDDLEWARE={
            'append': 'django.middleware.cache.FetchFromCacheMiddleware',
            'prepend': 'django.middleware.cache.UpdateCacheMiddleware',
        }):
            login_result = self.client.post(reverse("token_obtain_pair"), json.dumps(
                {
                    "username": "test",
                    "password": "test"
                }
            ), content_type="application/json")

            self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_result.data.get('access')}")
            result = self.client.get("/users/profile")
            self.assertEqual(result.status_code, 200)
            self.assertIsNone(result.data.get("full_name"))
            self.assertEqual(result.data.get("name_words"), 8)

            self.user.first_name = "new name"
            self.user.save()
            result = self.client.get("/users/profile")
            self.assertIsNone(result.data.get("full_name"))
