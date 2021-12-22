import os, re
import pandas as pd
import pprint
import json

NANO = '/usr/bin/nano'
nano = lambda x: os.spawnv(0, NANO, (NANO, x))

base_csv = 'csv/%s.csv'
def metadata(obj, pp=False):
  try:
    file = pd.read_csv(base_csv % obj._meta.model_name)
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

import json, re

def betadata(x):
    st, r = metadata(x)
    s = json.dumps(r)[1:-1]
    t = map(str.strip, s.split(','))
    u = iter(t)
    a = []
    b = 0
    for i in u:
        i = fix(i,b)
        v = '    '*b
        b += i.count('{')+i.count('[')-i.count('}')-i.count(']')
        a.append(v+i)
    a.extend(['' if not st else st[1:-1]])
    return '{\n%s}' % ',\n'.join(a)

def fix(z,b=0):
    y = re.findall('\{|\[',z)
    if y:
        x = re.split('\{|\[',z)
        n = [x[0]]
        for i in range(len(y)):
            n.append(y[i]+'\n'+'    '*(b+i+1))
            n.append(x[i+1])
        z = ''.join(n)
    a = re.findall('\}|\]',z)
    if a:
        x = re.split('\}|\]',z)
        n = [x[0]]
        a.reverse()
        x.reverse()
        t=[*range(len(a),0,-1)]
        c = b + len(y)
        for i in t:
            n.append('\n' +'    '*(c-t[i-1])+a[i-1])
            n.append(x[i-1])
        z=''.join(n)
    return z

def prep_req(method="GET"):
    from reactdev.settings import MIDDLEWARE
    import importlib
    from django.http import HttpRequest
    req = HttpRequest()
    req.method = method
    req.META['SERVER_NAME']='34.225.127.212'
    req.META['SERVER_PORT']='443'
    for middleware in MIDDLEWARE:
        try:
            x, y = middleware.rsplit('.', 1)
            m = getattr(importlib.import_module(x), y)
            m().process_request(req)
        except Exception as e:
            print(e)
    return req
