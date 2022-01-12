from .helpers import choices
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .model_factory import model_factory

AK, AKComment = model_factory('AK','AntiKink')
AP, APComment = model_factory('AP','AntiPornography')
PF, PFComment = model_factory('PF',"PornFree")
PFW, PFWComment = model_factory("PFW", "PornFreeWomen")
PHW, PHWComment = model_factory("PHW", "PornHatesWomen")
PIM, PIMComment = model_factory("PIM","PornIsMisogyny")

class Report(models.Model):
    content_type = models.ForeignKey(ContentType,
        to_field = 'id',
        on_delete = models.CASCADE,
    )
    object_id = models.SlugField(max_length=10)
    content_object = GenericForeignKey('content_type','object_id')
    created = models.DateTimeField(auto_now_add=True)
    action = models.SmallIntegerField(default=0)
    mod_action = models.IntegerChoices(value='action',names=('MARK_NSFW','DELETE'))
    author = models.ForeignKey(
        get_user_model(),
        to_field = 'id',
        on_delete=models.CASCADE,
        default=79,
    )

    def __str__(self):
        return str(self.content_object)

    def get_absolute_url(self):
        return self.content_object.get_absolute_url()

    def save(self, force_insert=False, force_update=False, using='default', update_fields=None):
        super().save(force_insert=False, force_update=False, using='default',update_fields=None)
        if self.action == 1:
            self.content_object.nsfw = True
            self.content_object.save(using='default',update_fields=['nsfw'])
        if self.action == 2:
            self.content_object.score = 1
            self.content_object.comments = 0
            self.content_object.save(using='default', update_fields=['score','comments'])
        if self.action > 3:
            choices = [a for a, b in choices(self.content_object._meta.model)]
            flair = choices[action]
            self.content_object.flair = flair
            self.content_object.save(using='default',update_fields=['flair'])

    def delete(self, using=None, keep_parents=False):
        klass = self.content_type.model_class()
        klass.objects.using('backup').get(id=self.object_id).save(using='default')
        return super().delete(using=None, keep_parents=False)

choices = (lambda x: [(j, j.name.lower()) for j in x.values() if hasattr(j, 'orphans')])(locals())
archives = {i._meta.model_name:i for i in [a for a, b in choices]}
comments = (lambda x: {j._meta.model_name:j for i, j in x.items() if 'Comment' in i})(locals())
