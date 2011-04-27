

import dream

import stats
import util


App = dream.App()

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
                data['queues'].extend([dict(server=server, queue=queue, **qstats) for queue, qstats in _data['queues'].iteritems()])

            data['servers'].sort(cmp=lambda x,y: cmp(x['server'].lower(), y['server'].lower()))
            data['queues'].sort(cmp=lambda x,y: cmp('%s.%s' % (x['server'].lower(), x['queue'].lower()), '%s.%s' % (y['server'].lower(), y['queue'].lower())))

    return dream.JSONPResponse(callback=callback, body=data)