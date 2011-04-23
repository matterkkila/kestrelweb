

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
    return util.render('index.html', {}, content_type='text/html')

@App.expose('/ajax/stats.json')
def ajax_stats(request):
    callback = request.str_params['callback'] if 'callback' in request.str_params else None
    servers = request.str_params['servers'].split(',')
    body = stats.get(servers)
    return dream.JSONPResponse(callback=callback, body=body)