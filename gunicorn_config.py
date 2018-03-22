worker_class = 'gevent'
worker_connections = 50
workers = 2

def pre_fork(server, worker):
    import psycogreen.gevent
    psycogreen.gevent.patch_psycopg()