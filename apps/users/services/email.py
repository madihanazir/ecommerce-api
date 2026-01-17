import uuid
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail

class EmailService:

    @staticmethod
    def generate_email_verification(user):
        token = uuid.uuid4()
        user.email_verification_token = token
        user.email_token_created_at = timezone.now()
        user.save()
        return token

    @staticmethod
    def send_verification_email(user, request):
        token = EmailService.generate_email_verification(user)

        verify_url = (
            f"{request.scheme}://{request.get_host()}"
            f"/api/v1/auth/verify-email/{token}/"
        )

        send_mail(
            subject="Verify your email",
            message=f"Click to verify: {verify_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return token
