#django
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import View
from django.shortcuts import get_object_or_404

#python
import logging
import pprint as pp

#app
from .helpers import choices
from .templatetags.custom_tags_archives import archive_pager
from reactdev.logging import CustomFormatter
from .views import create_report

# api views
from .serializers import PSerializer as PS, CSerializer as CS
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import status, csrf_exempt as rest_exempt


logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')
handler = logging.StreamHandler()
handler.setFormatter(
  CustomFormatter(
    '%(name)s - %(levelname)s - %(asctime)s - %(funcName)s - %(lineno)d - %(message)s',
    datefmt = '%m/%d/%Y %I:%M:%S %P',
  ))
handler.setLevel('DEBUG')
logger.addHandler(handler)

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
        if kwargs.get('id'):
            cserializer = CS(cmodel)(
                obj.comment_set.filter(id=kwargs['id']),
                context={'request':request},
                many=True
            )
        else:
            cserializer = CS(cmodel)(obj.orphans,
                context={'request':request},
                many=True
            )
        comments = cserializer.data
    response = Response({
        'post': post,
        'comments': comments,
        'comment_count':obj.comment_set.count(),
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

@api_view(['POST'])
def report_archive(request, *args, **kwargs):
    try:
        permission = request.get_signed_cookie('archives')
        logger.debug('signed cookie: %s', permission)
        if permission:
            return create_report(request, *args, **kwargs)
#            data = {
#                'flair': choices(kwargs['model']),
#            }
#        return Response(data, status=status.HTTP_200_OK)
    except KeyError:
        pass
    return Response(status=status.HTTP_401_UNAUTHORIZED)

class ArchiveAPIView(View):
    model = None
    def get(self, request, *args, **kwargs):
        if not kwargs.get('slug'):
            return archives_list(request, *args, **kwargs, model=self.model)
        return archives_detail(request, *args, **kwargs, model=self.model)

#    @csrf_exempt
    def post(self, request, *args, **kwargs):
        return report_archive(request, *args, **kwargs, model=self.model)
