

import gevent.monkey; gevent.monkey.patch_socket()
import gevent
import kestrel


def get(servers):
    def worker(server):
        return kestrel.Client(servers=[server], queue=None).stats()

    jobs = [gevent.spawn(worker, server) for server in servers]
    gevent.joinall(jobs)

    return dict([job.value for job in jobs])