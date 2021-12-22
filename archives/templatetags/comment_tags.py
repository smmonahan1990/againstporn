from django import template
from django.template import Template
from django.shortcuts import get_object_or_404
from django.utils.html import mark_safe
import re

def get_depth(object,depth=0):
    if object.parent_id:
        return get_depth(object.parent,depth=depth+1)
    return depth

def get_ancestor(object,depth=-5):
    if depth < 0:
        return get_ancestor(object.parent,depth=depth+1)
    return object.id

register = template.Library()

@register.simple_tag(takes_context=True)
def deleted(context):
    try:
        target = context['child']
    except KeyError:
        target = context['comment']
    if re.match('^\[(deleted|removed)\]$',target.body):
        if not target.children.count():
            return 'comment-deleted no-children'
        return 'comment-deleted'
    return ''

@register.simple_tag
def has_children(target):
    replies = target.children.exclude(body__regex='^\[(deleted|removed)\]$').count()
    if replies == 1:
        return mark_safe(' &middot; <span class="text-muted">1 reply</span>')
    if replies > 1:
        return mark_safe(' &middot; <span class="text-muted">{} replies</span>'.format(replies))
    return ''

@register.simple_tag(takes_context=True)
def recursion_depth(context):
    child = context['child']
    return get_depth(child)

@register.inclusion_tag(Template('{% include default %}'),takes_context=True)
def conditional_include(context,**kwargs):
    limit = 5
    obj = context['object']
    factor = context['request'].GET.get('page',1)
    id = context['request'].GET.get('id',None)
    if id:
        comment_model = obj.comment_set.model
        context.setdefault('child',get_object_or_404(comment_model, id=id))
    child = context['child']
    level = get_depth(child)
    if level > int(factor)*limit:
        if context.get('link_made') == child.parent.id:
            context['default'] = Template('')
        else:
            context['link_made'] = child.parent.id
            context['default'] = Template('<a href="?page={0}&id={2}">Continue reading</a>'.format(*divmod(level+limit,limit),child.parent.id))
    else:
        context['default'] = 'archive_child_comment.html'
    return context

@register.simple_tag(takes_context=True)
def ancestor_link(context):
    innerHTML = 'Comments continued from previous page.'
    page = context['request'].GET.get('page','2')
    id = context['request'].GET.get('id',None)
    object = context['object']
    try:
        if id and re.match('^\d+$',page) and int(page) > 2:
            comment_model = object.comment_set.model
            obj = get_object_or_404(comment_model, id=id)
            ancestor = get_ancestor(obj)
            return mark_safe('<a href="?page=%d&id=%s">%s</a>' % (int(page)-1,ancestor,innerHTML))
        elif id and int(page) == 2:
            path = context['request'].path.split('?')[0]
            return mark_safe(f'<a href="{path}">{innerHTML}</a>')
    except:
        pass
    return innerHTML
