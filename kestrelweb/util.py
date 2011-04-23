

import dream
import pystache


prefix = '/Users/merkkila/source/kestrelui'

def render(template_file, data=None, **kwargs):
    return dream.Response(body=pystache.render(template(template_file), data), **kwargs)

def static(filepath):
    return readfile('/static/%s' % filepath)

def template(filepath):
    return readfile('/templates/%s' % filepath)

def readfile(filepath):
    fp = open('%s%s' % (prefix, filepath))
    body = fp.read()
    fp.close()
    return body