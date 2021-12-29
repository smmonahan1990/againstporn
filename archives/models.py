
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .model_factory import model_factory

AK, AKComment = model_factory('AK','AntiKink')
AP, APComment = model_factory('AP','AntiPornography')
PF, PFComment = model_factory('PF',"PornFree")
PFW, PFWComment = model_factory("PFW", "PornFreeWomen")
PHW, PHWComment = model_factory("PHW", "PornHatesWomen")

class Report(models.Model):
    content_type = models.ForeignKey(ContentType,
        to_field = 'id',
        on_delete = models.CASCADE,
    )
    object_id = models.SlugField(max_length=10)
    content_object = GenericForeignKey('content_type','object_id')

    def __str__(self):
        return str(self.content_object)

    def get_absolute_url(self):
        return self.content_object.get_absolute_url()

    class Meta:
        unique_together = ['content_type','object_id']

choices = (lambda x: [(j, j.name.lower()) for j in x.values() if hasattr(j, 'orphans')])(locals())
archives = {i._meta.model_name:i for i in [a for a, b in choices]}
comments = (lambda x: {j._meta.model_name.split('comment')[0]:j for i, j in x.items() if 'Comment' in i})(locals())
