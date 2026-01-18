from django.test import TestCase


class SecurityTests(TestCase):
    def test_password_reset_does_not_leak_user(self):
        response = self.client.post(
            "/api/v1/auth/password/forgot/",
            {"email": "ghost@test.com"},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
