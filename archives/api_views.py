from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .helpers import choices
from django.db.models import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from .templatetags.custom_tags_archives import archive_pager

# api views
from .serializers import PSerializer as PS, CSerializer as CS
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def archives_detail(request, **kwargs):
    model = kwargs['model']
    comments = {}
    next, prev = '', ''
    obj = get_object_or_404(model, id=kwargs['slug'])
    next, prev = map(
        lambda x: x.get_absolute_url(),
        archive_pager({
           'object':obj,
           'request': request
        }).values()
    )
    pserializer = PS(model, **kwargs)(obj,
        context={'request':request},
        many=False
    )
    post = pserializer.data
    if obj.orphans:
        cmodel = obj.orphans.model
        cserializer = CS(cmodel)(obj.orphans.all(),
            context={'request':request},
            many=True
        )
        comments = cserializer.data
    response = Response({
        'post': post,
        'comments': comments,
        'next': next,
        'prev': prev,
    })
    return response

@api_view(['GET'])
def archives_list(request, **kwargs):
    data = []
    nextPage = 1
    previousPage = 1
    model = kwargs.get('model')
    handler = request.GET.copy()
    if handler.get('input'):
        model.objects.build_queryset(request, handler)
    archives = request.session.get(
        'queryset_%s' % model._meta.model_name, model.objects.queryset
    )
    page = handler.get('page',1)
    paginator = Paginator(archives, 25)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    serializer = PS(model)(
        data,
        context={'request':request},
        many=True
    )
    if data.has_next():
        nextPage = data.next_page_number()
    if data.has_previous():
        previousPage = data.previous_page_number()
    if isinstance(page, (int,str)) and int(page) == 1 and paginator.num_pages > 1:
        previousPage = paginator.num_pages
    response = Response({
        'data': serializer.data,
        'count': paginator.count,
        'numpages': paginator.num_pages,
        'nextlink': nextPage,
        'prevlink': previousPage,
        'flair': choices(model),
    })
    return response



