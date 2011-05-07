

import gevent.monkey; gevent.monkey.patch_socket()
import gevent
import kestrel


def action(command, server_queues):
    jobs = [
        gevent.spawn(getattr(kestrel.Client(servers=[server], queue=queue), command))
            for server, queue in server_queues
    ]
    gevent.joinall(jobs)

    return [job.value for job in jobs if job.value is not None]

def stats(servers):
    def worker(server):
        return kestrel.Client(servers=[server], queue=None).stats()

    jobs = [gevent.spawn(worker, server) for server in servers]
    gevent.joinall(jobs)

    results = [job.value for job in jobs if job.value is not None]
    if len(results):
        return dict(results)
    return None