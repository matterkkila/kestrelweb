

import gevent.monkey; gevent.monkey.patch_socket()
import gevent
import kestrel


def action(command, server_params):
    jobs = [
        gevent.spawn(getattr(kestrel.Client(servers=[server]), command), *params)
            for server, params in server_params
    ]
    gevent.joinall(jobs)

    return [job.value for job in jobs if job.value is not None]

def stats(servers):
    def worker(server):
        return kestrel.Client(servers=[server]).stats()

    jobs = [gevent.spawn(worker, server) for server in servers]
    gevent.joinall(jobs)

    results = [job.value for job in jobs if job.value is not None]
    if len(results):
        return dict(results)
    return None