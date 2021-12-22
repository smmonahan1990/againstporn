from django import template
from django.template import Template
from django.utils.safestring import mark_safe
import re
from archives.models import Archive
from PIL import Image
register = template.Library()
sub = {'&amp;':'&','&quot;':'"','&#039;':"'"}
def clean_selftext(string):
    new_string = re.sub(r'&amp;(?:#x200B|nbsp);|\\','',string)
    new_string = re.sub('(?m:^“ ?(.+?)(?:[”“]\s*$))',lambda x: '&gt;{}\n\n'.format(x.group(1)),new_string)
    new_string = re.sub('(?m:(?<=^&gt; )(\s+)|(^&gt;\s+$))','',new_string)
    new_string = re.sub('(?:\s*\n\s*){3,}','\n\n',new_string)
    new_string = re.sub('(?m:(^|(?:(?<!\])\()|\s)(https?://(?:([^\s\(\)]+?)|(\S*?\([^\s\)]+?\)\S*?)))([^\w/]?(?=\s|$)))',lambda x: '%s[%s](%s)%s' % (x.group(1),x.group(2),x.group(2),x.group(5)),new_string)
    return new_string
styles = {'~~(.+?)~~':'del',
    '\B\*\*([^\*\n]+)\*\*\B':'b',
    '\B\*([^\*\n]+)\*\B':'i',
    '(?s:^(?:>|&g?t;)([^!].+?)(\n{2}(?!&g?t;)|$))': 'blockquote',
    '(?s:&gt;!(.+?)!&lt;)':'spoiler',
    '^(?:\-|\*) (?!\W+$)(.+)':'li',
    '(?s:(<li>.+?</li>)(?=\n(?!<li>)|$))':'ul',
    '^##+\s*(.+)':'h5'
    }

sup='\^+\((.+?\)?)\)|(?<!_)\^[\^#]*((?:[^_\-\s\^\(\)<][^\s\^\<>]*)|(?:<[^>]+>\S+</[^>]+>))'
rule = lambda x, y: '<%(y)s>%(x)s</%(y)s>' % {'x':x.group(1),'y':y}
markdown_link = re.compile('\[(?P<alias>([^\[\]]+?)|(.*?\[[^\[\]]+?\].*?))\]\((?P<url>([^\(\s\)]+?)|(\S*?\([^\(\s\)]+?\)\S*?))\)(?=\W|\s|$)') 
markdown_rule = '<a href="%(url)s">%(alias)s</a>'
@register.filter
def apply_styles(text):
    try:
        text = re.sub('^\s+','',text.replace('\n\n','\n'))
        text = clean_selftext(text)
        for key, value in styles.items():
            text = re.sub(key, lambda k: rule(k,value), text,flags=re.MULTILINE)
        text = re.sub('(?<=[^\n])\n(?=[^\n])','\n\n',text)
        markdown = markdown_link.finditer(text)
        for i in markdown:
            text = text.replace(i.group(0), markdown_rule % i.groupdict())
        text = re.sub('^\s*[\*\-]+\s*$',mark_safe('<div class="dropdown-divider mt-3 mb-3"></div>'),text,flags=re.MULTILINE)
        text = re.sub('\^+\((.+?\)?)\)|(?<!_)\^[\^#]*((?:[^_\-\s\^\(\)<][^\s\^\<>]*)|(?:<[^>]+>\S+</[^>]+>))',lambda x: '<sup>%s</sup>' % tuple(filter(lambda y: bool(y),[x.group(1),x.group(2)])),text)
        text = re.sub('</sup> *<sup>',' ',text)
        text = re.sub('(?<=</sup>)(\s*)(<a[^>]+?><sup>)',lambda x: ' '+x.group(2),text)
        text = re.sub('</blockquote>(\s+)?<blockquote>','\n',text)
        text = re.sub('(?<=\S)(\s+)(?=<blockquote>)','',text)
        text = re.sub('(?<=</h5>)\s*(?=<div class="dropdown)','',text)
        text = re.sub('</(?P<tag>\w+)>\s+<(?P=tag)>',lambda x: '</%(tag)s><%(tag)s>' % x.groupdict(), text)
        text = re.sub('</ul>\s*?<ul>','',text)
        text = re.sub('({}|{}|{})'.format(*sub.keys()),lambda x: sub[x.group()],text)
    except TypeError:
        pass
    return mark_safe(text.strip())

@register.inclusion_tag(Template('{% include default %}'), takes_context = True)
def toggle_preview(context):
    matchstr = r'^\[(https?://\S+?)\]\(([h/]\S+?)\)$'
    try:
        link = context['link']
    except KeyError:
        link = context['post']
    if not link.selftext and not link.fullsize:
        if issubclass(type(link), Archive):
            context['default'] = Template('')
        else:
            context['default'] = 'button_link_svg.html'
    else:
        context['default'] = 'button_%s_svg.html' % ('img' if link.fullsize else ('link','text')[not re.match(matchstr, clean_selftext(link.selftext).lstrip())])
    return context

imgur = re.compile(r'^\s*\[?https?://(?:www\.)?(?:[im]\.)?imgur\.com/(?P<prefix>(a|gallery)/)?(?P<url>\w+)(?=.*$)')
youtube = re.compile(r'^\s*\[?https?://((((m|www)\.)?youtube\.com/watch\?v=)|youtu\.be/)(?P<link>[\w-]+)\S*?\s?$')
from django.utils.html import format_html
@register.filter
def embedded(post):
     markup = ''.join(['<blockquote class="imgur-embed-pub" lang="en"',
                       ' data-id="{prefix}{url}"  ><a href="//imgur.com/{prefix}{url}">',
                       '</a></blockquote><script async ',
                       'src="//s.imgur.com/min/embed.js"',
                       ' charset="utf-8"></script>'])
     yt = ''.join(['<iframe width="560" height="315" ',
                   'src="https://www.youtube.com/embed/{link}"',
                   ' title="YouTube video player" frameborder="0"',
                   ' allow="accelerometer; autoplay; clipboard-write; ',
                   'encrypted-media; gyroscope; picture-in-picture" ',
                   'allowfullscreen></iframe>'])
     match = imgur.search(str(post.selftext)) or youtube.search(str(post.selftext))
     if match:
         if 'link' in match.groupdict().keys():
              return mark_safe(yt.format(**match.groupdict()))
         y = match.groupdict().copy()
         y.update({'prefix':('a/','')[not y['prefix']]})
         return mark_safe(markup.format(**y))
     if post.__class__.__name__=='Post':
         return '[%(link)s](%(link)s)' % vars(post)
     return post.selftext

@register.simple_tag(takes_context=True)
def has_img(context):
    link = context.get(('object','post')[bool(context.get('post'))])
    if issubclass(type(link),Archive):
        if link.fullsize or (bool(link.selftext) and (imgur.search(link.selftext) or youtube.search(link.selftext))):
            return 'post-has-img%s' % ('',' nsfw')[link.flair == 'WARNING: GORE' or (isinstance(link.flair,str) and link.flair.upper().startswith('NSFW'))]
    else:
        if isinstance(link.link,str) and (youtube.search(link.link) or imgur.search(link.link)):
            return 'has-img%s' % ('',' has-embedded nsfw')[bool(link.nsfw)]
        elif link.fullsize:
            return 'has-img%s' % ('',' nsfw')[bool(link.nsfw)]
    return ''

