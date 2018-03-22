worker_class = 'gevent'
worker_connections = 50
workers = 2
preload_app = True

def pre_fork(server, worker):
    import gevent.monkey
    import psycogreen.gevent
    gevent.monkey.patch_all()
    psycogreen.gevent.patch_psycopg()