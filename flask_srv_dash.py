from time import time, sleep
import threading
from datetime import datetime

import requests
from flask import current_app, g, request
from tzlocal import get_localzone

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

class SrvDashBackgroundWorkerThread(threading.Thread):
    """
        Simple background thread that sends the logs
        every 30 secs.
    """
    def __init__(self, app_uri, auth_enabled=False, auth_key=None):
        threading.Thread.__init__(self)
        self.app_uri = app_uri
        self.auth_enabled = auth_enabled
        self.auth_key = auth_key
        self.lock = threading.Lock()
        self.logs = []

    def send_logs(self):
        with self.lock:
            if not self.logs: # no logs to send
                return
            headers = {
                'Content-Type': 'application/json',
            }
            if self.auth_enabled:
                headers['X-Auth-Key'] = self.auth_key
            try:
                http_response = requests.post(self.app_uri + '/add_data', json=self.logs, headers=headers)
            except Exception as e:
                pass
            finally:
                self.logs = []

    def add_log_item(self, log_item):
        with self.lock:
            self.logs.append(log_item)

    def run(self):
        while True:
            sleep(30)
            self.send_logs()


class SrvDashExtension(object):
    def __init__(self, app, app_name, app_uri, auth_enabled=False, auth_key=None):
        self.app = app
        self.app_name = app_name
        self.app_uri = app_uri
        self.auth_enabled = auth_enabled
        self.auth_key = auth_key
        self.worker = SrvDashBackgroundWorkerThread(app_uri, auth_enabled=auth_enabled, auth_key=auth_key)
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.before_request(self.before_req)
        app.after_request(self.after_req)
        self.worker.daemon = True
        self.worker.start()

    def process_request(self, req_resp_meta_data):
        self.worker.add_log_item(req_resp_meta_data)

    def after_req(self, response):
        response_meta_data = {
            'status-code': response.status_code,
            'resp-time': int((time() - g.srv_dash_req_start_time) * 1000),
            'resp-Date': datetime.now(get_localzone()).isoformat(),
            'resp-Content-Length': int(response.headers.get('Content-Length', 0)),
            'resp-Content-Type': response.headers.get('Content-Type', ''),
        }
        g.srv_dash_req_resp_meta_data.update(response_meta_data)
        self.process_request(g.srv_dash_req_resp_meta_data)
        return response

    def before_req(self):
        g.srv_dash_req_start_time = time()
        g.srv_dash_req_resp_meta_data = {
            'app': self.app_name,
            'scheme': 'http' if request.url.startswith('http://') else 'https',
            'method': request.method,
            'path': request.path,
            'ip': request.remote_addr,
            'req-Date': datetime.now(get_localzone()).isoformat(),
            'req-Content-Length': int(request.headers.get('Content-Length', 0)) if type(request.headers.get('Content-Length')) == str else 0,
            'req-Content-Type': request.headers.get('Content-Type', ''),
            'Origin': request.headers.get('Origin', ''),
            'User-Agent': request.headers.get('User-Agent', ''),
        }
