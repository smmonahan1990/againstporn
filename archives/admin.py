import pandas as pd
from django.urls import path
from django.shortcuts import reverse, get_object_or_404
from django.db.models import Q
from django.contrib import admin
from django.contrib.admin import register
from django.contrib.admin.decorators import action, display
from django.contrib.admin.options import csrf_protect_m
from django.template.defaultfilters import linebreaks, mark_safe
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from .models import Report, archives, comments
from .forms import ReportForm, CustomModelFormFactory as CMF
from .helpers import choices
from helpers import m, CL
from .templatetags.custom_tags_archives import archive_pager
from templates.templatetags.custom_tags import apply_styles, embedded
from datetime import datetime as dt, timezone as tz, timedelta as td
from reactdev.settings import BASE_DIR

# Register your models here.

logger = CL(__name__)

class ReportListFilter(admin.SimpleListFilter):
    title = 'category'
    parameter_name = 'category'
    def lookups(self, request, model_admin):
        return (('comments','Comments'),('posts','Posts'),)

    def queryset(self, request, queryset):
        if self.value() == 'comments':
            return queryset.filter(content_type__model__in=comments.keys())
        if self.value() == 'posts':
            return queryset.filter(content_type__model__in=archives.keys())
        return queryset

@register(Report)
class AdminReport(admin.ModelAdmin):
    form = ReportForm
    list_filter = (ReportListFilter,)

class CustomFilter(admin.SimpleListFilter):

    def __init__(self, request, params, model, model_admin):
        self.model = model
        super().__init__(request, params, model, model_admin)

class StatusFilter(CustomFilter):
    title = parameter_name = 'status'

    def lookups(self, request, model_admin):
        return ((i, i) for i in ['published','unpublished', 'reported'])

    def queryset(self, request, queryset):
        if self.value() == 'published':
            return self.model.objects.queryset
        if self.value() == 'unpublished':
            return self.model.manager.filter(Q(comments=0)&Q(score=1))
        if self.value() == 'reported':
            return self.model.objects.exhaustive.using('backup')

class YearFilter(CustomFilter):
    title = parameter_name = 'year'

    def lookups(self, request, model_admin):
        interval = self.model.objects.exhaustive.order_by('submitted')
        low = '{:%Y}'.format(interval.first().submitted)
        high = '{:%Y}'.format(interval.last().submitted)
        return ((str(i), i) for i in range(int(low), int(high)+1))

    def queryset(self, request, queryset):
        for key, val in self.lookups(request, model_admin=None):
            if self.value() == key:
                from_date = dt(val,1,1,0,0,0,tzinfo=tz.utc)
                to_date = from_date + td(days=(365,366)[key in ['2020','2016']])
                return queryset.filter(
                    submitted__range=[from_date,to_date]
                )

class ScoreFilter(CustomFilter):
    title = parameter_name = 'score'
    def lookups(self, request, model_admin):
        vals = [[-1,0],[50,1000],[100,1000]]
        keys = ['< 1', '≥ 50', '≥ 100']
        return list(zip(vals, keys))

    def queryset(self, request, queryset):
        for key, val in self.lookups(request, model_admin=None):
            if self.value() == str(key):
                return queryset.filter(Q(score__gt=key[0])&Q(score__lt=key[1]))

class FlairFilter(CustomFilter):
    title = parameter_name = 'flair'

    def lookups(self, request, model_admin):
        return choices(self.model)

    def queryset(self, request, queryset):
        for key, val in self.lookups(request, model_admin=None):
            if self.value() == key:
                return queryset.filter(flair=val)

class CategoryFilter(CustomFilter):
    title = parameter_name = 'category'

    def lookups(self, request, model_admin):
        return (('fullsize','Image',),('selftext','Text'),)
    def queryset(self, request, queryset):
        for key, val in self.lookups(request,model_admin=None):
            if self.value() == key:
                return queryset.filter(**{'%s__isnull' % key: False})

class NSFWFilter(CustomFilter):
    pass

@register(*archives.values())
class ArchiveAdmin(admin.ModelAdmin):
    list_display = ['title','submitted','user','score','comments']
    list_filter = (StatusFilter, YearFilter, ScoreFilter, FlairFilter, CategoryFilter)
    readonly_fields = ['title','submitted','user','score','comments','metadata', 'post']
    list_per_page=50
    search_fields = ['author','title','selftext']
    fieldsets = (
       ('Editable Fields',
         {
          'classes': ('editable','collapse', 'd-none',),
          'fields': ('nsfw','flair','status')
        ,}),
       ('Summary',
         {
          'classes':('summary','collapse', 'd-none',),
          'fields': ('title','user','submitted','score','comments',)
        ,}),
       ('Post body',
         {
          'classes':('post-body','collapse', 'd-none',),
          'fields':('post',),
         }),
       ('Metadata',
         {
          'classes':('metadata','collapse', 'd-none',),
          'fields': ('metadata',),
         }),
    )

    def get_fieldsets(self, request, obj):
        if obj.fullsize or not embedded(obj) == obj.selftext:
            fieldsets = self.fieldsets
            fieldsets[2][1]['classes'] = ('post-image','collapse', 'd-none',)
            return fieldsets
        return self.fieldsets

    @display(description="author", ordering="author")
    def user(self, obj):
        querystring = '?author=%s' % obj.author
        path = reverse('admin:%s_%s_changelist' % (obj._meta.app_label,obj._meta.model_name))
        return mark_safe(f'<a id="filter_user" href="{path}{querystring}">{obj.author}</a>')

    def metadata(self, obj):
        return mark_safe('<iframe id="json" height="350" src="../json/"></iframe>')

    def post(self, obj):
        if obj.selftext:
            return mark_safe(linebreaks(apply_styles(embedded(obj))))
        if obj.fullsize:
            return mark_safe(
              ''.join([
               '<div style="display:flex;justify-content:center;align-items:center;">',
               '<img class="img-fluid" style="display:none;" src="/static/',
               f'{obj.fullsize}',
               '" /></div>'
            ])
        )

    def get_changelist_instance(self, request):
        cli = super().get_changelist_instance(request)
        if request.GET.get('author'):
            cli.has_active_filters = True
            cli.clear_all_filters_qs = '?'
        return cli

    def get_search_fields(self, request, *args, **kwargs):
        if request.GET.get('author'):
            return self.search_fields[:1]
        return self.search_fields

    def get_form(self, *args, **kwargs):
        return CMF(self.model)

    def get_urls(self):
        urls = super().get_urls()
        exclude = '%s_%s_add' % (self.model._meta.app_label, self.model._meta.model_name)
        from django.urls import path
        urls = [i for i in urls if not i.name == exclude]
        urls.insert(0,path('<path:object_id>/json/',self.json_view, name='%s_json' % self.model._meta.model_name,))
        return urls

    @xframe_options_exempt
    @csrf_protect_m
    def json_view(self, request, *args, **kwargs):
        if request.user.is_staff:
            try:
                x = get_object_or_404(self.model.manager,id=kwargs['object_id'])
                x = '{\n    %s\n}' % '\n    '.join(m(x).split('\n')[1:-1])
                return HttpResponse(
                    mark_safe(
                     linebreaks(
                       '<div style="font-size:10px;font-family:monospace;white-space:break-spaces;">%s</div>' % x
                )))
            except TypeError as e:
                    logger.error(locals())
            return HttpResponse('stuff will go here!')
        else:
            next = reverse('admin:%s_json' % self.model._meta.model_name, args=(kwargs['object_id'],))
            return HttpResponseRedirect('%s?next=%s' % (reverse('admin:login'), next))

    def get_queryset(self, request, *args, **kwargs):
        return self.model.manager.all()

    class Media:
        css = {
            'all': ('css/adminstyles.css',),
        }
        js = ['js/customadmin.js','js/customviewport.js','js/customlink.js']


    def save_model(self, request, obj, form, change):
        logger.debug(locals())
        result = super().save_model(request,obj, form, change)
        logger.debug(locals())
        return result

    def save_related(self, request, form, formsets, change):
        logger.debug(vars(form))
        result = super().save_related(request,form, formsets, change)
        logger.debug(locals())
        logger.debug(vars(form))
        return result

    def save_form(self, request, form, change):
        logger.debug(locals())
        result = super().save_form(request, form, change)
        logger.debug(locals())
        logger.debug(vars(result))
        return result
