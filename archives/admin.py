from django.urls import path
from django.contrib import admin
from django.contrib.admin import register
from .models import Report
from .forms import ReportForm
from django.http import HttpResponse
# Register your models here.

class ReportListFilter(admin.SimpleListFilter):
    title = 'category'
    parameter_name = 'category'
    def lookups(self, request, model_admin):
        return (
            ('comments','Comments'),
            ('posts','Posts'),
        )
    def queryset(self, request, queryset):
        if self.value() == 'comments':
            return queryset.filter(content_type_id__in=[9,10])
        if self.value() == 'posts':
            return queryset.filter(content_type_id__in=[6,7])
        return queryset

@register(Report)
class AdminReport(admin.ModelAdmin):
    form = ReportForm
    list_filter = (ReportListFilter,)
