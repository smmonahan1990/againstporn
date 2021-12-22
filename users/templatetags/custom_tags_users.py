from django import template
import os

register = template.Library()

@register.filter
def condition_on_env(url):
#    url = 'http://34.225.127.212%s/api/accounts/'
    try:
        setting = os.environ.get('DJANGO_SETTINGS_MODULE','reactdev.dev')
        if setting == 'reactdev.dev':
#        return url % ':8000'
            return url.replace('/api', ':8000/api')
        return url
    except:
        return url
