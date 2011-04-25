

import os

import dream
import pystache


prefix = os.path.normpath('%s/../..' % (os.path.realpath(__file__)))


def render(template_file, data=None):
    return pystache.render(template(template_file), data)

def static(filepath):
    return readfile('/static/%s' % filepath)

def template(filepath):
    return readfile('/templates/%s' % filepath)

def readfile(filepath):
    fp = open('%s%s' % (prefix, filepath))
    body = fp.read()
    fp.close()
    return body