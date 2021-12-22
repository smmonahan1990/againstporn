from django.urls import path
from django.conf.urls import url
from .api_views import archives_detail, archives_list
from .models import choices

apipatterns = [url(r'^%s/$' % i.name.lower(), archives_list, {'model':i}) for i, j in choices]
apipatterns +=[path(r'%s/<slug:slug>/' % i.name.lower(), archives_detail, {'model':i}) for i, j in choices]
