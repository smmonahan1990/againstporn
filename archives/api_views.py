#django
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.admin.options import get_content_type_for_model
from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType
from django.views.generic import View
from django.shortcuts import get_object_or_404, reverse

#python
import logging
import pprint as pp

#app
from .helpers import choices
from .templatetags.custom_tags_archives import archive_pager
from reactdev.logging import CustomFormatter
#from .views import create_report
from .forms import ReportForm

# api views
from .serializers import PSerializer as PS, CSerializer as CS, WriteablePSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.views import status, csrf_exempt as rest_exempt

from reactdev.logging_config import CustomLogger as CL
logger = CL(__name__)

@api_view(['GET'])
def archives_detail(request, **kwargs):
    model = kwargs['model']
    next, prev = '', ''
    obj = get_object_or_404(model.manager.using('default'), id=kwargs['slug'])
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
    cmodel = obj.orphans.model
    cset = obj.orphans if not kwargs.get('id') else obj.comment_set.filter(id=kwargs['id'])
    cserializer = CS(cmodel)(
        cset,
        context=dict(request=request),
        many=True
    )
    response = Response({
        'post': pserializer.data,
        'comments': cserializer.data,
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
@permission_classes([IsAdminUser,])
def report_archive(request, *args, **kwargs):
    if not kwargs.get('slug'):
        return Response({'success':request.user.is_staff},status=status.HTTP_200_OK)
    instance = get_object_or_404(kwargs['model'].manager, id=kwargs['slug'])
    if not request.data.get('action'):
        resp_data=reverse('admin:%s_%s_change' % (instance._meta.app_label, instance._meta.model_name), args=(kwargs['slug'],))
        response = Response({'success':resp_data},status=status.HTTP_200_OK)
        return response
    serializer = WriteablePSerializer(kwargs['model'])
    try:
        instance_serializer = serializer(
          data=request.data,
          instance=instance,
          many=False
        )
        if instance_serializer.is_valid():
            instance_serializer.save()
            return Response({'success':'moderation recorded.'}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(e)
        return Response({'detail':e},status=status.HTTP_400_BAD_REQUEST)

class ArchiveAPIView(View):
    model = None
    def get(self, request, *args, **kwargs):
        if not kwargs.get('slug'):
            return archives_list(request, *args, **kwargs, model=self.model)
        return archives_detail(request, *args, **kwargs, model=self.model)

    def post(self, request, *args, **kwargs):
        kwargs.update(model=self.model)
        return report_archive(request, *args, **kwargs)
