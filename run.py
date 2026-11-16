"""Render web service entry point.

Keeps a small HTTP server alive on $PORT so UptimeRobot can ping the service,
and runs bot.py alongside it, restarting it if it ever exits.
"""

import http.server
import json
import os
import shutil
import subprocess
import sys
import threading
import time

PORT = int(os.environ.get("PORT", "10000"))
START_TIME = time.time()


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/status":
            payload = {
                "service": "monlua-bot",
                "system_node": bool(shutil.which("node")),
                "ironveil_v1": os.path.isfile(".runtime/vendor/ironveil/index.js") and bool(shutil.which("node")),
                "77fuscator": os.path.isfile(".runtime/77fuscator/deobfuscator.dll") and os.path.isfile(".runtime/dotnet/dotnet"),
                "ironbrew2": os.path.isfile(".runtime/vendor/ironbrew2/LuaAnalysis.Ironbrew2.dll") and os.path.isfile(".runtime/dotnet/dotnet"),
                "dotnet_8": os.path.isdir(".runtime/dotnet/shared/Microsoft.NETCore.App/8.0.0") or any(name.startswith("8.") for name in os.listdir(".runtime/dotnet/shared/Microsoft.NETCore.App")) if os.path.isdir(".runtime/dotnet/shared/Microsoft.NETCore.App") else False,
                "dotnet_9": any(name.startswith("9.") for name in os.listdir(".runtime/dotnet/shared/Microsoft.NETCore.App")) if os.path.isdir(".runtime/dotnet/shared/Microsoft.NETCore.App") else False,
                "oracle_configured": bool(os.environ.get("ORACLE") or os.environ.get("IRONBREW2_ORACLE_KEY")),
                "v151_tool": os.path.isfile("deobf/v151/deob.js"),
                "v151_luau": os.path.isfile("deobf/v151/bin/luau") and os.access("deobf/v151/bin/luau", os.X_OK),
                "v151_luau_ast": os.path.isfile("deobf/v151/bin/luau-ast") and os.access("deobf/v151/bin/luau-ast", os.X_OK),
                "centurion_tool": os.path.isfile("deobf/centurion/centurion.py"),
                "v151_node_archive": os.path.isfile("deobf/v151/vendor/node-v20.19.5-linux-x64.tar.gz"),
                "uptime_seconds": int(time.time() - START_TIME),
                "cloud_runner": bool(os.environ.get("GH_DISPATCH_TOKEN")),
            }
            body = json.dumps(payload).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"MonLua Bot is running")

    def do_HEAD(self):
        # UptimeRobot checks with HEAD; answer 200 so the ping keeps the
        # free instance awake and the monitor stays green.
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def log_message(self, *args):
        pass


server = http.server.ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
print(f"Keep-alive server listening on port {PORT}", flush=True)

while True:
    code = subprocess.call([sys.executable, "bot.py"])
    print(f"bot.py exited with code {code}, restarting in 30s", flush=True)
    time.sleep(30)
