import os, re, json
import pandas as pd
import pprint
import json
import importlib
import glob
from typing import List, Text, Union
from pathlib import PosixPath
from reactdev.settings import BASE_DIR, MIDDLEWARE
from django.http import HttpRequest
from django.db.models import Q
from django.contrib.auth import login
from users.models import CustomUser as CU
from rest_framework.authentication import TokenAuthentication as TA
from django.apps import apps
from reactdev.logging_config import CustomLogger as CL

logger = CL(__name__)

NANO = '/usr/bin/nano'
_nano = lambda x: os.spawnv(0, NANO, (NANO, x))

exc = '/usr/bin/%s'
spawn = lambda x, *y: os.spawnv(0, exc % x, (exc % x, *y))

def nano(filename):
    try:
        _nano(glob.glob(filename)[0])
    except IndexError:
        _nano(filename)

def to_file(l: List, filename: Text) -> None:
    file = PosixPath(BASE_DIR / 'txt' / ('%s.txt' % filename))
    if not file.exists():
        file.touch()
    file.write_text('\n'.join(l))

def to_list(filename: Text) -> Union[List, None]:
    if PosixPath(filename).exists():
        return list(map(str.strip, open(filename)))

def metadata(obj, pp=False):
  base_csv = 'csv/%s/%s.csv'
  try:
#    file = pd.read_csv('../%s' % (base_csv % (obj.name.lower(),obj._meta.model_name)), low_memory=False)
    file = pd.read_csv(BASE_DIR / (base_csv % (obj.name.lower(),obj._meta.model_name)), low_memory=False)
    row = file.loc[file['id']==obj.id]
    cols = sorted(list(set(row.columns).difference({'selftext'})))
    st = row.selftext.to_list()[0]
    data = row[cols].to_dict('records')[0]
    data = {i: j for i, j in data.items() if not isinstance(j, float) and not j in ['[]','{}',[],{},False]}
    printer = pprint.PrettyPrinter()
    st = None if isinstance(st, float) else printer.pformat({'selftext':st})
    if pp:
        return st, printer.pformat(data)
    return st, data
  except Exception as e:
    print(e.with_traceback(e.__traceback__))

def betadata(x):
    st, r = metadata(x)
    s = json.dumps(r)[1:-1]
    t = map(str.strip, s.split(','))
    u = iter(t)
    a = []
    b = 0
    for i in u:
#        n, i = fix(i,b)
#        b += n
        if not re.search('[\'"]\s?:',i):
            n, i = fix(i, b)
            b += n
            a = a[:-1] + [a[-1]+', '+ i]
            continue
        n, i = fix(i,b)
        v = '    '*b
        b += n
#        b += i.count('{')+i.count('[')-i.count('}')-i.count(']')
        a.append(v+i)
    a += [] if not st else [st[1:-1]]
    return '{\n%s\n}' % ',\n'.join(a)

def fix(z,b=0):
    y = re.findall('\{(?!\})|\[(?!\])',z)
    if y:
        x = re.split('\{(?!\})|\[(?!\])',z)
        n = [x[0]]
        for i in range(len(y)):
            n.append(y[i]+'\n'+'    '*(b+i+1))
            n.append(x[i+1])
        z = ''.join(n)
    a = re.findall('(?<!\{)\}|(?<!\[)\]',z)
    if a:
        x = re.split('(?<!\{)\}|(?<!\[)\]',z)
        n = [x[0]]
        a.reverse()
        x.reverse()
        t=[*range(len(a),0,-1)]
        c = b + len(y)
        for i in t:
            n.append('\n' +'    '*(c-t[i-1])+a[i-1])
            n.append(x[i-1])
        z=''.join(n)
    return len(y) - len(a), z

def prep_req(method="GET", auth=True, headers=True):
    req = HttpRequest()
    req.method = method
    req.META['SERVER_NAME'] = '34.225.127.212'
    req.META['SERVER_PORT'] = '80'
    req.META['REMOTE_ADDR'] = os.environ['SSH_CLIENT'].split(' ')[0]
    req.META['SCRIPT_NAME'] = ''
    for middleware in MIDDLEWARE:
        try:
            x, y = middleware.rsplit('.', 1)
            m = getattr(importlib.import_module(x), y)
            m().process_request(req)
        except Exception as e:
            pass
    if auth:
        user = CU.objects.get(id=1)
        login(req, user)
    if headers:
        req.META['HTTP_AUTHORIZATION'] = 'Token %s' % user.auth_token.key
    return req

from datetime import datetime as dt, timezone as tz, timedelta as td
import logging

class CustomFormatter(logging.Formatter):
    @staticmethod
    def converter(*args, **kwargs):
        cst = tz(td(hours=-6),'CST')
        return dt.now(tz=cst).timetuple()

def config_logging():
   logger = logging.getLogger('debugger')
   [logger.removeHandler(i) for i in logger.handlers]
   handler = logging.StreamHandler()
   handler.setFormatter(CustomFormatter("%(name)s - %(levelname)s - %(asctime)s %(module)s - %(lineno)d - %(message)s", datefmt='%m/%d/%Y %I:%M:%S %P'))
   handler.setLevel('DEBUG')
   logger.setLevel('DEBUG')
   logger.addHandler(handler)
   return logger

def get_json(qs, check=True):
    if check:
        qs = qs.filter(json__isnull=True)
    n = 0
    for i in qs:
        try:
            i.json = '{\n    %s\n}' % '\n    '.join(betadata(i).split('\n')[1:-1])
            i.save(update_fields=['json'])
            n += 1
            if divmod(n, 50)[1] == 0:
                logger.debug('%d of %d %s updated.', n, qs.count(), qs.model._meta.verbose_name_plural.lower())
        except Exception as e:
            logger.error(e)
    logger.debug('program completed with %d successful updates and %d failures.', n, qs.count()-n)

def prep_form():
#    pass
    from django.contrib.admin import site
    from archives.models import PF as pf
    from archives.admin import ArchiveAdmin as AA
    obj = pf.manager.filter(Q(submitted__gt='2022-01-01')&Q(title='test')).first()
    request = prep_req()
    form = AA(pf, site)
    return obj, request, form

