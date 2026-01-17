import uuid
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings

class PasswordService:

    @staticmethod
    def generate_reset_token(user):
        token = uuid.uuid4()
        user.password_reset_token = token
        user.password_token_created_at = timezone.now()
        user.save()
        return token

    @staticmethod
    def send_reset_email(user, request):
        token = PasswordService.generate_reset_token(user)

        reset_url = (
            f"{request.scheme}://{request.get_host()}"
            f"/api/v1/auth/password/reset/{token}/"
        )

        send_mail(
            subject="Password Reset Request",
            message=f"Reset your password using this link:\n{reset_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

    @staticmethod
    def is_token_valid(user):
        if not user.password_token_created_at:
            return False
        return timezone.now() <= user.password_token_created_at + timedelta(hours=1)
