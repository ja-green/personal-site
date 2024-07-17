import multiprocessing

user = "www"
group = "www"

max_requests = 1000
max_requests_jitter = 50

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1

accesslog = "-"
errorlog = "-"
loglevel = "info"
capture_output = True

keyfile = "/etc/ssl/internal/app-key.pem"
certfile = "/etc/ssl/internal/app-cert.pem"
ca_certs = "/etc/ssl/internal/ca.pem"


def ssl_context(conf, default_ssl_context_factory):
    import ssl

    context = default_ssl_context_factory()
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    context.verify_mode = ssl.CERT_REQUIRED
    return context
