
from django.db import models
from django.shortcuts import reverse
from django.utils.html import mark_safe
from django.template.defaultfilters import truncatechars
from .managers import ArchiveManager
# Create your models here.

class Archive(models.Model):
    name = ''
#    nsfw = models.BooleanField(null=True, blank=True)
    selftext = models.TextField(null=True,blank=True)
    fullsize = models.CharField(max_length=255,null=True,blank=True)
    thumbnail = models.CharField(max_length=255,null=True,blank=True)
    title = models.SlugField(max_length=350)
    author = models.CharField(max_length=50)
    flair = models.CharField(max_length=255,null=True,blank=True)
    submitted = models.DateTimeField(auto_now_add=False)
    score = models.CharField(max_length=10,null=True,blank=True)
    comments = models.PositiveIntegerField(null=True,blank=True)
    id = models.SlugField(max_length=6,primary_key=True)
    json = models.JSONField(null=True, blank=True)
    objects = ArchiveManager()

    def get_absolute_url(self):
        return reverse(self.name.lower(), args = [self.id,])

    def __str__(self):
        return self.title

    @property
    def is_removed(self):
        return self.score in [1, '1'] and self.comments == 0

    @property
    def orphans(self):
        return self.comment_set.exclude(parent_id__isnull=False)

    class Meta:
        abstract = True
        ordering = ['-id',]

class Comment(models.Model):
    author = models.CharField(max_length=50)
    id = models.SlugField(max_length=10,primary_key=True)
    body = models.TextField()
    score = models.IntegerField(null=True,blank=True)
    date = models.DateTimeField(auto_now_add=False)
    text = models.CharField(max_length=255,null=True,blank=True)
    bgcolor = models.CharField(max_length=50,null=True,blank=True)
    color = models.CharField(max_length=50,null=True,blank=True)
    css_class = models.CharField(max_length=50,null=True,blank=True)

    @property
    def user_flair(self):
        return '' if not all(getattr(self,i) for i in ['css_class','color','bgcolor','text',]) else mark_safe(
            '<span class="user-flair %(css_class)s" style="background-color:%(bgcolor)s;border-color:%(bgcolor)s!important;color:%(color)s!important;">%(text)s</span>' % vars(self)
        )

    @property
    def is_downvoted(self):
        return isinstance(self.score, int) and self.score < 1

    def __str__(self):
        return '%s: %s' % (self.author,truncatechars(self.body,100))

    def get_absolute_url(self):
        return reverse(self.post.name.lower(), args = [self.post_id,self.id,])

    class Meta:
        abstract = True

class AK(Archive):
    name = 'AntiKink'

class AKComment(Comment):
    post = models.ForeignKey(AK,
        on_delete = models.CASCADE,
        to_field = 'id',
        related_name = 'comment_set',
    )
    parent = models.ForeignKey('archives.AKComment',
        on_delete = models.DO_NOTHING,
        parent_link = True,
        related_name = 'children',
        null = True,
        blank = True,
    )

class AP(Archive):
    name = 'AntiPornography'

class APComment(Comment):
    post = models.ForeignKey(AP,
        on_delete = models.CASCADE,
        to_field = 'id',
        related_name = 'comment_set',
    )
    parent = models.ForeignKey('archives.APComment',
        on_delete = models.DO_NOTHING,
        parent_link = True,
        related_name = "children",
        null = True,
        blank = True,
    )

from django.db.models import F
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

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

#    def save(self, *args, **kwargs):
#        object = self.content_object
#        if issubclass(type(object),Archive):
#            if object.is_removed:
#                object.score = None
#                object.save()
#            else:
#                object.comments = 0
#                object.score = 1
#                object.save()
#        else:
#            if not object.score:
#                object.score = -1
#                object.save()
#            else:
#                object.score = -1 * int(object.score)
#                object.save()
#        super().save(*args,**kwargs)

choices = (lambda x: [(j, i.lower()) for i, j in x.items() if hasattr(j, 'orphans') and not i == 'Archive'])(locals())
