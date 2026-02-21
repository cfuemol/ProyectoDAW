import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
timeout = 120
keepalive = 5
bind = "0.0.0.0:8000"

accesslog = "-"
errorlog = "-"
loglevel = "info"
