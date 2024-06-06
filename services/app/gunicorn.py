import multiprocessing

user = "www"
group = "www"

max_requests = 1000
max_requests_jitter = 50

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1

keyfile = "/etc/ssl/internal/app-key.pem"
certfile = "/etc/ssl/internal/app-cert.pem"
ca_certs = "/etc/ssl/internal/ca.pem"
