"""Render web service entry point.

Keeps a small HTTP server alive on $PORT so UptimeRobot can ping the service,
and runs bot.py alongside it, restarting it if it ever exits.
"""

import http.server
import os
import subprocess
import sys
import threading
import time

PORT = int(os.environ.get("PORT", "10000"))


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"MonLua Bot is running")

    def log_message(self, *args):
        pass


server = http.server.ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
print(f"Keep-alive server listening on port {PORT}", flush=True)

while True:
    code = subprocess.call([sys.executable, "bot.py"])
    print(f"bot.py exited with code {code}, restarting in 30s", flush=True)
    time.sleep(30)
