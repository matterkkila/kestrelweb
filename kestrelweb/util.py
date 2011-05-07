

import os
import re

PREFIX = os.path.normpath('%s/../..' % (os.path.realpath(__file__)))

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

def static(filepath):
    return readfile('/html/static/%s' % filepath)

def template(filepath):
    return readfile('/templates/%s' % filepath)

def readfile(filepath):
    fp = open('%s%s' % (PREFIX, filepath))
    body = fp.read()
    fp.close()
    return body