

import gevent.monkey; gevent.monkey.patch_socket()
import gevent
import kestrel


def flush(servers, queue):
    def worker(server, queue):
        return kestrel.Client(servers=[server], queue=queue).flush()

    jobs = [gevent.spawn(worker, server, queue) for server in servers]

    results = [job.value for job in jobs if job.value is not None]
    return results

def delete(servers, queue):
    def worker(server, queue):
        return kestrel.Client(servers=[server], queue=queue).delete()

    jobs = [gevent.spawn(worker, server, queue) for server in servers]

    results = [job.value for job in jobs if job.value is not None]
    return results

def get(servers):
    def worker(server):
        return kestrel.Client(servers=[server], queue=None).stats()

    jobs = [gevent.spawn(worker, server) for server in servers]
    gevent.joinall(jobs)

    results = [job.value for job in jobs if job.value is not None]
    if len(results):
        return dict(results)
    return None