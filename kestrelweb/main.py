

import dream

import local_settings
import kestrel_actions
import util


App = dream.App()


@App.expose('/')
def home(request):
    return dream.Response(body=util.template('index.html'), content_type='text/html')


@App.expose('/ajax/action.json')
def ajax_action(request):
    callback = request.str_params['callback'] if 'callback' in request.str_params else None
    action = request.str_params['action'] if 'action' in request.str_params else None
    server_queue = request.str_params.getall('server') if 'server' in request.str_params else []

    data = {}
    status = 200

    if len(server_queue) == 0:
        data['error'] = 'Missing server or queue name'
        status = 500
    elif action in ['flush', 'delete', 'peek', 'flush_all', 'reload', 'shutdown']:
        actions = []
        for _sq in server_queue:
            (server, queue) = _sq.split(',', 1) if _sq.count(',') else (_sq, None)
            actions.append((server, queue))
        data['results'] = kestrel_actions.action(action, actions)
    else:
        data['error'] = 'Invalid action'
        status = 500

    return dream.JSONResponse(callback=callback, body=data, status=status)


@App.expose('/ajax/stats.json')
def ajax_stats(request):
    callback = request.str_params['callback'] if 'callback' in request.str_params else None
    servers = request.str_params['servers'] if 'servers' in request.str_params else None
    qsort = request.str_params['qsort'] if 'qsort' in request.str_params else None
    qreverse = int(request.str_params['qreverse']) if 'qreverse' in request.str_params else 0
    qfilter = request.str_params['qfilter'] if 'qfilter' in request.str_params else None

    response = {}
    if servers:
        server_stats = dict([(server, None) for server in servers.split(',')])
        queue_stats = []

        stats_response = kestrel_actions.stats(server_stats.iterkeys())
        if stats_response is not None:
            for server, _data in stats_response.iteritems():
                server_stats[server] = _data['server']
                queue_stats.extend([
                    dict(server=server, queue=queue, **qstats)
                        for queue, qstats in _data['queues'].iteritems()
                            if util.queue_filter(qfilter, queue, qstats)
                ])

        response['servers'] = [
            {'server': server, 'stats': _stats}
                for server, _stats in server_stats.iteritems()
        ]
        response['servers'].sort(key=util.QUEUE_SORT['server'])

        response['queues'] = queue_stats
        response['queues'].sort(key=util.QUEUE_SORT['server'])
        response['queues'].sort(key=util.QUEUE_SORT[qsort] if qsort in util.QUEUE_SORT else util.QUEUE_SORT['name'], reverse=qreverse)

    return dream.JSONResponse(callback=callback, body=response)


@App.expose('/ajax/config.json')
def templates(request):
    callback = request.str_params['callback'] if 'callback' in request.str_params else None

    return dream.JSONResponse(callback=callback, body={
        'servers': [{'server': server} for server in local_settings.servers],
        'templates': {
            'content': util.template('content.html'),
            'servers': util.template('servers.html'),
            'queues': util.template('queues.html'),
        }
    })

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