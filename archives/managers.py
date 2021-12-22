from django.db import models
from django.db.models import Q
import time

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

