from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Report, archives
from django.contrib.admin.models import LogEntry
from datetime import datetime as dt, timezone as tz, timedelta as td
import logging, pprint as pp
from reactdev.logging_config import CustomLogger as CL

for key, value in archives.items():
    locals()[key] = value

logger = CL(__name__)
#logger = logging.getLogger(__name__)

@receiver(post_save, sender=Report)
def flag_reported(sender, instance, **kwargs):
    logger.debug('Signal received by post_save signal handler from sender Report.')
    logger.debug('listing local variables:')
    logger.debug(locals())
    cst = tz(td(hours=-6), 'CST')
    LogEntry.objects.create(
        content_type_id=8,
        object_id=instance.id,
        action_time=dt.now(tz=cst),
        action_flag=1,
        user_id=79,
        change_message = "Report created: %s" % str(instance)
    )

@receiver(pre_save, sender=Report)
def archive_reported(sender, instance, **kwargs):
    logger.debug('Signal received by pre_save signal handler from sender %s', sender.__name__)
    logger.debug('local variables:')
    logger.debug(locals())
    instance.content_object.save(using='backup')

@receiver(pre_save, sender=pfw)
@receiver(pre_save, sender=phw)
@receiver(pre_save, sender=pf)
@receiver(pre_save, sender=ap)
@receiver(pre_save, sender=ak)
@receiver(pre_save, sender=pim)
def log_update(sender, instance, **kwargs):
    if kwargs.get('update_fields'):
        logger.debug(
          '%s post changed. fields updated: %s',
          instance._meta.model_name,
          kwargs['update_fields']
        )
    logger.debug(locals())
