from django.db import models
from django.db.models import Q, Count, F
from helpers import CL
import time

logger = CL(__name__)

score_dict = {
    'opt1': r'^0',
    'opt2': r'(?:1,?\d|[1-9])\d{2}',
    'opt3': r'(?:1,?\d{2}|2[5-9]|[3-9]\d)\d',
    'opt4': r'(?:1,?\d[5-9])\d{2}',
    'opt5': r'1,?\d{3}',
}

class ArchiveManager(models.Manager):
    def get_queryset(self,**kwargs):
        queryset = super().get_queryset()
        if not kwargs.get('no_votes_comments'):
            queryset = queryset.exclude(Q(score=1)&Q(comments=0))
        return queryset

    queryset = property(get_queryset)

    @property
    def exhaustive(self):
        return self.get_queryset(no_votes_comments=True)

    def set_comments(self, *args, **kwargs):
        qs = self.annotate(Count('comment_set')).exclude(comment_set__count=F('comments'))
        if qs:
            logger.debug('updating comment fields of %d %s.', qs.count(), self.model._meta.verbose_name_plural)
            [self.filter(id=i.id).update(comments=i.comment_set__count) for i in qs]
        else:
            logger.debug('all clean.')

    def from_df(self,df,*args,**kwargs):
        n = self.exhaustive.count()
        df.drop(df.loc[df['id'].isin(self.exhaustive.values_list('id',flat=True))].index, inplace=True)
        self.bulk_create(self.model(**i) for i in df.to_dict('records'))
        m = self.exhaustive.count()
        logger.debug('%d new %s created.', m-n, self.model._meta.verbose_name_plural)

    def validate_dtformat(func):
        def innerfunc(self, request, params):
            keys = [i for i in params.keys() if '_date' in i]
            if keys:
                for i in keys:
                    try:
                        time.strptime(params[i],'%Y-%m-%d')
                    except ValueError:
                        params.pop(i)
            func(self, request, params)
        return innerfunc

    @validate_dtformat
    def build_queryset(self,request,params):
        keys = ['flair','title__contains','author__contains','submitted__gt','submitted__lt','selftext__contains','comments__gte','comment_set__author__contains','comment_set__body__contains']
        values = list(map(params.get,['flair','title','author','from_date','to_date','selftext','comments','comment_author','comment_body']))
        args_dict = dict(filter(lambda x: x[1],zip(keys,values)))
        if params.get('score'):
            args_dict.update(score__regex=score_dict[params['score']])
        if params.get('category'):
            args_dict.update({'%s__isnull' % params['category']:False})
        sign = '' if params.get('sort_asc') else '-'
        queryset = self.get_queryset(**params).filter(**args_dict).order_by('%sid' %  sign)
        if {'comment_body','comment_author'}.intersection(list(params)):
            queryset = queryset.distinct()
        request.session['queryset_%s' % self.model._meta.model_name] = queryset

class CommentManager(models.Manager):

    def delete_removed(self):
        n = self.count()
        x = 1
        while x > 0:
            x, y = self.annotate(Count('children')).filter(Q(children__count=0)&Q(body__regex='^\[(deleted|removed)\]$')).delete()
        m = self.count()
        logger.debug('%d comments deleted.',n-m)

    def bulk_create(self, *args, **kwargs):
        n = self.count()
        super().bulk_create(*args, **kwargs)
        self.delete_removed()
        m = self.count()
        logger.debug('%d new comments created.', m-n)

    def from_df(self, df, *args, **kwargs):
        df.drop(df.loc[df['id'].isin(self.values_list('id',flat=True))].index, inplace=True)
        self.bulk_create(self.model(**i) for i in df.to_dict('records'))
