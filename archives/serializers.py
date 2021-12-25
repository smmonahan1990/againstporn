from rest_framework import serializers
from templates.templatetags.custom_tags import apply_styles, embedded
from django.template.defaultfilters import linebreaks, mark_safe
import re

# serialize posts

def PSerializer(post_model, **kwargs):
    selftext = serializers.SerializerMethodField()
    submitted = serializers.SerializerMethodField()
    json = serializers.SerializerMethodField()
    def get_selftext(self, obj):
        if obj.selftext is not None:
            styles = 'class="d-flex justify-content-center align-items-center"'
            st = linebreaks(apply_styles(embedded(obj))).replace('<p><iframe',f'<p {styles}><iframe')
            if re.search('class="(imgur|twitter)', st):
                st = mark_safe(f'<div {styles}>{st}</div>')
            return st
    def get_submitted(self,obj):
        return '{:%b %d, %Y, %I:%M %P.}'.format(obj.submitted).replace(' 0',' ')
    def get_json(self, obj):
        return linebreaks(mark_safe(obj.json.replace('\\\'','')))
    def get_fields():
        if kwargs:
            return ['comments','author','title','selftext','fullsize','submitted','flair','json']
        return ['score','comments','author','title','submitted','flair','id','thumbnail']
    class Meta:
        model = post_model
        fields = get_fields()

    attrs = {
        '__module__':'archives.serializers',
        'Meta':Meta,
        'submitted':submitted,
        'get_submitted':get_submitted,
    }
    if kwargs:
        attrs.update({
            'selftext':selftext,
            'get_selftext':get_selftext,
            'json':json,
            'get_json': get_json,
        })
    name = '%sSerializer' % post_model.__name__
    serializer = type(name, (serializers.ModelSerializer,), attrs)
    return serializer


# serialize comments

def CSerializer(comment_model):
    body = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField(read_only=True)

    def get_body(self, obj):
        if obj.body is not None:
            return linebreaks(apply_styles(obj.body))

    def get_date(self,obj):
        return '{:%b %d, %Y, %I:%M %P.}'.format(obj.date).replace(' 0',' ')

    def get_children(self, obj):
        if obj.children is not None:
            data = []
            for child in obj.children.all():
                data.append(self.__class__(child).data)
            return data
        else:
            return None

    class Meta:
        model = comment_model
        fields = ('id', 'body','score','author','date','children', 'text')

    attrs = {
        '__module__': 'archives.serializers',
        'Meta': Meta,
        'body': body,
        'get_body': get_body,
        'date': date,
        'get_date': get_date,
        'children': children,
        'get_children': get_children,
    }
    name = '%sSerializer' % comment_model.__name__
    serializer = type(name, (serializers.ModelSerializer,),attrs)
    return serializer


