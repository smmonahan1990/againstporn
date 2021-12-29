def choices(model):
    flair_choices = list(model.objects.exclude(flair__isnull=True).values_list('flair',flat=True))
    return sorted([(i, i) for i in set(flair_choices) if flair_choices.count(i) > 1])

import re
sub_dict={'&amp;':'&','&quot;':'"','&lt;':'<','&gt;':'>','&amp;#x200B;':''}
def resub(string):
    new_string = re.sub('(&(?:amp(?:;#x200B)?|quot|lt|gt);)',lambda x: sub_dict.get(x.group(1),''), string)
    return new_string
