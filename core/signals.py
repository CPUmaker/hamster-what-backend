from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.template.loader import render_to_string
from django.urls import reverse
from knox.models import AuthToken

from core.models.profile import Profile


@receiver(post_save, sender=User)
def create_related_profile(sender, instance, created, *args, **kwargs):
    if instance and created:
        # create profile for new user
        instance.profile = Profile.objects.create(user=instance)
        # reset user's status to inactive
        instance.is_active = False


@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, *args, **kwargs):
    # send an e-mail to the user
    if instance and created:
        context = {
            'current_user': instance,
            'username': instance.username,
            'email': instance.email,
            'domain': 'localhost:8000',
            'token': AuthToken.objects.create(instance)[0].digest
        }

        # render email text
        email_html_message = render_to_string('email/user_verification.html', context)

        msg = EmailMessage(
            # title:
            "User Verification for {title}".format(title="Some website title"),
            # message:
            email_html_message,
            # from:
            "noreply@somehost.local",
            # to:
            [instance.email]
        )
        msg.send()

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)

    msg = EmailMessage(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_html_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.send()
