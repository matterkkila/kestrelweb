

import re

import dream

import stats
import util


App = dream.App()


QUEUE_SORT = {
    'server': lambda x: x['server'].lower(),
    'name': lambda x: x['queue'].lower(),
    'items': lambda x: x['items'],
    'bytes': lambda x: x['bytes'],
    'total_items': lambda x: x['total_items'],
    'logsize': lambda x: x['logsize'],
    'expired_items': lambda x: x['expired_items'],
    'mem_items': lambda x: x['mem_items'],
    'mem_bytes': lambda x: x['mem_bytes'],
    'age': lambda x: x['age'],
    'discarded': lambda x: x['discarded'],
    'waiters': lambda x: x['waiters'],
    'open_transactions': lambda x: x['open_transactions'],
}

FILTER_COMP = {
    '=': lambda x, y: x == y,
    '>': lambda x, y: x > y,
    '<': lambda x, y: x < y,
    '>=': lambda x, y: x >= y,
    '<=': lambda x, y: x <= y,
    '!=': lambda x, y: x != y,
}

def queue_filter(pattern, queue, qstats):
    """A filter to restrict queues"""
    try:
        if (pattern is not None) and isinstance(pattern, (str, unicode)) and (len(pattern) > 0):
            _m = re.match('(.*?)(>=|<=|!=|=|<|>)(.*)', pattern)
            if not _m:
                return True

            (field, comp, filter_value) = _m.groups()

            value = None
            if field == 'queue':
                value = queue
            elif field in qstats:
                value = qstats[field]
            else:
                raise Exception('Unknown field')

            if comp not in FILTER_COMP:
                raise Exception('Unknown comparitor')

            if isinstance(value, (int, long, float)):
                if FILTER_COMP[comp](value, float(filter_value)):
                    return True
            elif isinstance(value, (str, unicode)):
                if comp not in ['!=', '=']:
                    raise Exception('Invalid comparitor')

                qmatch = re.match(filter_value, value, re.I)
                if qmatch and (comp == '='):
                    return True
                elif not qmatch and (comp == '!='):
                    return True

                return False
            else:
                raise Exception('Unknown type')

            return False
    except:
        pass

    return True

@App.expose('/static/<filepath:.*>')
def static(request, filepath):
    body = ''
    content_type = 'test/plain'

    try:
        body = util.static(filepath)
        if filepath.endswith('.css'):
            content_type = 'text/css'
        elif filepath.endswith('.js'):
            content_type = 'text/javascript'
        elif filepath.endswith('.html'):
            content_type = 'text/html'
    except:
        pass

    return dream.Response(body=body, content_type=content_type)

@App.expose('/')
def home(request):
    return dream.Response(body=util.template('index.html'), content_type='text/html')

@App.expose('/ajax/stats.json')
def ajax_stats(request):
    callback = request.str_params['callback'] if 'callback' in request.str_params else None
    servers = request.str_params['servers'] if 'servers' in request.str_params else None
    qsort = request.str_params['qsort'] if 'qsort' in request.str_params else None
    qreverse = int(request.str_params['qreverse']) if 'qreverse' in request.str_params else 0
    qfilter = request.str_params['qfilter'] if 'qfilter' in request.str_params else None

    data = {}
    if servers:
        servers = servers.split(',')
        _stats = stats.get(servers)

        if _stats is not None:
            data = dict([
                ('servers', []),
                ('queues', [])
            ])

            for server, _data in _stats.iteritems():
                data['servers'].append({'server': server, 'stats': _data['server']})
                data['queues'].extend([dict(server=server, queue=queue, **qstats) for queue, qstats in _data['queues'].iteritems() if queue_filter(qfilter, queue, qstats)])

            data['servers'].sort(cmp=lambda x,y: cmp(x['server'].lower(), y['server'].lower()))
            data['queues'].sort(key=QUEUE_SORT['server'])
            data['queues'].sort(key=QUEUE_SORT[qsort] if qsort in QUEUE_SORT else QUEUE_SORT['name'], reverse=qreverse)

    return dream.JSONPResponse(callback=callback, body=data)