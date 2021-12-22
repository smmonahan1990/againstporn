from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Report
from django.contrib.admin.models import LogEntry
from datetime import datetime as dt, timezone as tz

@receiver(post_save, sender=Report)
def flag_reported(sender, instance, **kwargs):
    LogEntry.objects.create(
        content_type_id=8,
        object_id=instance.id,
        action_time=dt.now(),
        action_flag=1,
        user_id=4,
        change_message = "Report created: %s" % str(instance)
    )
