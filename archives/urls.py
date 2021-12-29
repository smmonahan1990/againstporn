from django.urls import re_path
from django.conf.urls import url
from .api_views import ArchiveAPIView
from django.views.decorators.csrf import csrf_exempt
from .models import choices

apipatterns = [re_path(r'^%s/(?:(?P<slug>\w{6})/(?:(?P<id>\w{7})/)?)?' % j, csrf_exempt(ArchiveAPIView.as_view(model=i))) for i, j in choices]
