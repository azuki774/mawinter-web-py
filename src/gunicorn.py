import os
import json

# TCPソケット
socket_path = "0.0.0.0:" + str(os.getenv("PORT", 9876))
bind = socket_path

# Debugging
reload = True

# Logging
accesslog = "-"
access_log_format = json.dumps(
    {
        "remote_address": r"%(h)s",
        "user_name": r"%(u)s",
        "date": r"%(t)s",
        "status": r"%(s)s",
        "method": r"%(m)s",
        "url_path": r"%(U)s",
        "query_string": r"%(q)s",
        "protocol": r"%(H)s",
        "response_length": r"%(B)s",
        "referer": r"%(f)s",
        "user_agent": r"%(a)s",
        "request_time_seconds": r"%(L)s",
    }
)
# loglevel = 'info'
loglevel = "debug"
logfile = "./log/app.log"
logconfig = None

# Proc Name
proc_name = "Infrastructure-Practice-Flask"

# Worker Processes
workers = 2
worker_class = "sync"
