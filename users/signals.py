from django.contrib import auth
from django.dispatch import receiver
from django.core.signals import request_started
from django.db.models.signals import post_save, post_delete
from authemail.models import SignupCode, PasswordResetCode
import logging
import pprint as pp
from datetime import datetime as dt, timezone as tz

logger = logging.getLogger(__name__)

@receiver(auth.user_logged_in)
def log_user_in(sender, request, user, **kwargs):
    logger.debug('User {} logged in through page {}'.format(
        user.username or user.email.split('@')[0],
        request.META.get('HTTP_REFERER')
    ))

@receiver(auth.user_logged_out)
def log_user_out(sender, request, user, **kwargs):
    logger.debug('User {} logged out. Session duration: {}'.format(
        user.username or user.email.split('@')[0],
        dt.now(tz=tz.utc)-user.last_login
    ))

@receiver(post_save, sender=SignupCode)
def account_created(sender, instance, **kwargs):
    logger.debug('New account created for %s' % instance.user.email)

@receiver(post_save, sender=PasswordResetCode)
def password_reset_code_created(sender, instance, **kwargs):
    logger.debug('Password reset code %d generated for %s' % (instance.id, instance.user.email))

@receiver(post_delete, sender=PasswordResetCode)
def password_reset_code_deleted(sender, instance, **kwargs):
    logger.debug(f"Password reset code {instance.pk} for %s destroyed %s after it was created." % (
        instance.user.email,
        '{:%H hours, %M minutes}'.format(
            dt.fromtimestamp(
                dt.now(tz=tz.utc).timestamp() -
                instance.created_at.timestamp()
            )
        )
    ))

@receiver(post_delete, sender=SignupCode)
def signup_code_deleted(sender, instance, **kwargs):
    logger.debug(f"Signup code {instance.pk} for %s destroyed %s after it was created." % (
        instance.user.email,
        '{:%H hours, %M minutes}'.format(
            dt.fromtimestamp(
                dt.now(tz=tz.utc).timestamp() -
                instance.created_at.timestamp()
            )
        )
    ))

#@receiver(request_started)
#def inspect_request(sender, environ, **kwargs):
#    logger.debug(
#        pp.pformat(
#            environ,
#        )
#    )
#
