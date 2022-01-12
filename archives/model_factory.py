
from django.db import models
from django.shortcuts import reverse
from django.template.defaultfilters import truncatechars
from django.utils.html import mark_safe
from emoji import demojize
from .managers import ArchiveManager, CommentManager
# Create your models here.

STATUS_CHOICES = models.IntegerChoices(
 'status', names=(
  'PUBLISHED','UNPUBLISHED','REPORTED',
 ))


def model_factory(klass, long_name):
    class Archive(models.Model):
        name = long_name
        status = models.IntegerField(choices=STATUS_CHOICES.choices, default=1,null=True, blank=True)
        nsfw = models.BooleanField(null=True, blank=True)
        selftext = models.TextField(null=True, blank=True)
        fullsize = models.CharField(max_length=255, null=True, blank=True)
        thumbnail = models.CharField(max_length=255, null=True, blank=True)
        title = models.CharField(max_length=350,null=True, blank=True)
        author = models.CharField(max_length=50,null=True,blank=True)
        flair = models.CharField(max_length=255, null=True, blank=True)
        submitted = models.DateTimeField(auto_now_add=False,null=True,blank=True)
        score = models.IntegerField(default=1, null=True, blank=True)
        comments = models.PositiveIntegerField(null=True, blank=True)
        id = models.SlugField(max_length=6, primary_key=True)
        json = models.TextField(null=True, blank=True)
        objects = ArchiveManager()
        manager = models.QuerySet(using='default').as_manager()

        def get_absolute_url(self):
            return reverse('frontend', args = [self.name.lower(), self.id,])

        def __str__(self):
            return demojize(self.title)

        @property
        def orphans(self):
            return self.comment_set.exclude(parent_id__isnull=False)

        class Meta:
            abstract = True
            ordering = ['-id',]
            verbose_name = f'{long_name} Post'
            verbose_name_plural = f'{long_name} Posts'

    class Comment(models.Model):
        awards = models.CharField(null=True, blank=True, max_length=255)
        author = models.CharField(max_length=50)
        id = models.SlugField(max_length=10,primary_key=True)
        body = models.TextField()
        score = models.IntegerField(null=True,blank=True)
        date = models.DateTimeField(auto_now_add=False)
        text = models.CharField(max_length=255,null=True,blank=True)
        bgcolor = models.CharField(max_length=50,null=True,blank=True)
        color = models.CharField(max_length=50,null=True,blank=True)
        css_class = models.CharField(max_length=50,null=True,blank=True)
        objects = CommentManager()
        post = models.ForeignKey(f'archives.{klass}',
            on_delete = models.CASCADE,
            to_field = 'id',
            related_name = 'comment_set',
        )
        parent = models.ForeignKey(f'archives.{klass}Comment',
            on_delete = models.DO_NOTHING,
            parent_link = True,
            related_name = 'children',
            null = True,
            blank = True,
        )
        @property
        def user_flair(self):
            return '' if not all(getattr(self,i) for i in ['css_class','color','bgcolor','text',]) else mark_safe(
                '<span class="user-flair %(css_class)s" style="background-color:%(bgcolor)s;border-color:%(bgcolor)s!important;color:%(color)s!important;">%(text)s</span>' % vars(self)
            )

        @property
        def is_downvoted(self):
            return isinstance(self.score, int) and self.score < 1

        def __str__(self):
            try:
                return '%s: %s' % (self.author, demojize(truncatechars(self.body,100)))
            except TypeError:
                return super().__str__()

        def get_absolute_url(self):
            return reverse('frontend', args=[self.post.name.lower(),self.post_id,self.id,])

        class Meta:
            abstract = True
            verbose_name = f'{long_name} Comment'
            verbose_name_plural = f'{long_name} Comments'

    ArchiveModel = type(klass, (Archive,), {'__module__':'archives.models'})
    CommentModel = type(f'{klass}Comment', (Comment,), {'__module__':'archives.models'})
    return (ArchiveModel, CommentModel)

#AP, APComment = model_factory('AP', 'AntiPornography')
#AK, AKComment = model_factory('AK', 'AntiKink')
