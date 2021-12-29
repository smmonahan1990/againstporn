from django import template
from django.template import Template
from django.utils.safestring import mark_safe
from archives.models import choices
from django.db.models import Q
from emoji import demojize
import re

subdict = {'&amp;':'&','&quot;':'"','&gt;':'>','&lt;':'<','&amp;#x200B;':''}
def resub(substr):
    new_string = re.sub('(&(?:amp(?:;#200xB)?|quot|lt|gt);)',lambda x: subdict.get(x.group(1),''),substr)
    return new_string

register = template.Library()

@register.inclusion_tag('navlinks.html',takes_context=True)
def navlinks(context):
    return {'models': [i for i, j in choices], 'request':context['request']}

@register.simple_tag(takes_context=True)
def display_flair(context):
    object = context['link']
    if object.flair:
        return mark_safe('<span class="TNH">%s</span>' % object.flair)
    return ''

@register.inclusion_tag('archives_pager.html',takes_context=True)
def archive_pager(context, **kwargs): # do not use in posts
    obj, req = map(context.get,['object','request'])
    qs = kwargs.get('reset') or req.session.get('queryset_%s' % obj._meta.model_name, type(obj).objects.queryset).order_by('submitted')
    queue = list(qs.values_list('id',flat=True))
    try:
        idx = queue.index(obj.id)
    except ValueError:
        try:
            return archive_pager(context, reset=type(obj).objects.order_by('submitted'),**kwargs)
        except KeyError:
            reset = type(obj).objects.exhaustive.filter(Q(id=obj.id)|~Q(Q(comments=0)&Q(score=1))).order_by('submitted')
            return archive_pager(context,reset=reset,**kwargs)
    next = dict(enumerate(queue)).get(idx+1,queue[0]) # search wraps
    previous = queue[idx-1]
    return {'next':type(obj).objects.get(id=next),'previous':type(obj).objects.get(id=previous)}


from django.contrib.contenttypes.models import ContentType as CT
from archives.forms import ReportForm

@register.inclusion_tag(Template('{% include default %}'), takes_context=True)
def report(context, obj):
    user = context['request'].user
    if user.is_authenticated and user.has_perm('archives.add_report'):
        content_type_id = CT.objects.get(model=obj._meta.model_name, app_label='archives').id
        object_id = obj.id
        context['report_form'] = ReportForm(initial={'content_type':content_type_id,'object_id':object_id})
        context['default'] = 'reportform.html'
    else:
        context['default'] = Template('')
    return context

