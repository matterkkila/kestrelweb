

import os


prefix = os.path.normpath('%s/../..' % (os.path.realpath(__file__)))


def static(filepath):
    return readfile('/static/%s' % filepath)

def template(filepath):
    return readfile('/templates/%s' % filepath)

def readfile(filepath):
    fp = open('%s%s' % (prefix, filepath))
    body = fp.read()
    fp.close()
    return body