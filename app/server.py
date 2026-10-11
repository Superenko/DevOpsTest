import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ENV_NAME = os.getenv("ENV_NAME", "local")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            code = 200
            body = json.dumps(
                {"status": "ok", "service": "app", "env": ENV_NAME},
                separators=(",", ":"), 
            ).encode()
        else:
            code = 404
            body = b'{"error":"not found"}'
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        rid = self.headers.get("X-Request-ID", "-")
        print(f"rid={rid} {self.address_string()} {fmt % args}", flush=True)


ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()