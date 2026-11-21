"""Render web service entry point.

Keeps a small HTTP server alive on $PORT so UptimeRobot can ping the service,
and runs bot.py alongside it, restarting it if it ever exits.
"""

import html as html_module
import http.server
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import urllib.request
from pathlib import Path

PORT = int(os.environ.get("PORT", "10000"))
START_TIME = time.time()


class Handler(http.server.BaseHTTPRequestHandler):
    RUBIS_RAW_API = "https://api.rubis.app/v2/scrap/{scrap_id}/raw"

    def _serve_rubis_raw(self, scrap_id: str) -> None:
        if not re.fullmatch(r"[A-Za-z0-9_-]{4,64}", scrap_id):
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"unknown scrap")
            return
        try:
            request = urllib.request.Request(
                self.RUBIS_RAW_API.format(scrap_id=scrap_id),
                headers={"User-Agent": "monlua-bot/2.0"})
            with urllib.request.urlopen(request, timeout=10) as response:
                body = response.read()
        except Exception:
            body = b""
        if not body:
            self.send_response(502)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"could not fetch the Rubis scrap")
            return
        accept = self.headers.get("Accept", "")
        if "text/html" in accept:
            # Browsers (Discord's in-app one included) download plain-text
            # links, so navigations get a real HTML viewer instead; HttpGet
            # callers still get the identical raw bytes.
            page = (
                "<!doctype html><html><head><meta charset='utf-8'>"
                "<meta name='viewport' content='width=device-width, initial-scale=1'>"
                f"<title>Rubis raw &middot; {scrap_id}</title>"
                "<style>body{margin:0;background:#0A0A0E;color:#E6E6F0}"
                "header{padding:10px 16px;font:600 13px/1 system-ui;color:#9C7CFF;"
                "border-bottom:1px solid #23232B}"
                "pre{margin:0;padding:14px 16px;white-space:pre-wrap;word-break:break-word;"
                "font:13px/1.55 ui-monospace,Menlo,Consolas,monospace}</style></head>"
                f"<body><header>Rubi&scaron; raw &middot; {scrap_id}</header>"
                "<pre>" + html_module.escape(body.decode("utf-8", errors="replace")) + "</pre></body></html>"
            )
            data = page.encode("utf-8")
            out_type = "text/html; charset=utf-8"
        else:
            data = body
            out_type = "text/plain; charset=utf-8"
        self.send_response(200)
        self.send_header("Content-Type", out_type)
        self.send_header("Content-Disposition", "inline")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path.startswith("/rubis/"):
            self._serve_rubis_raw(path[len("/rubis/"):].strip("/"))
            return
        if path == "/status":
            runtime = Path(".runtime")
            dotnet_shared = runtime / "dotnet" / "shared" / "Microsoft.NETCore.App"
            dotnet_versions = [item.name for item in dotnet_shared.iterdir()] if dotnet_shared.is_dir() else []
            payload = {
                "service": "monlua-bot",
                "system_node": bool(shutil.which("node")),
                "ironveil_v1": (runtime / "vendor/ironveil/deobfuscator/index.js").is_file() and (bool(shutil.which("node")) or (runtime / "node/bin/node").is_file()),
                "77fuscator": (runtime / "77fuscator/deobfuscator.dll").is_file() and (runtime / "dotnet/dotnet").is_file() and any(version.startswith("8.") for version in dotnet_versions) and ((runtime / "java/bin/java").is_file() or bool(shutil.which("java"))) and Path("deobf/bin/unluac.jar").is_file(),
                "ironbrew2": (runtime / "vendor/ironbrew2/LuaAnalysis.Ironbrew2.dll").is_file() and (runtime / "vendor/ironbrew2/runtimes/linux-x64/native/liblua54.so").is_file() and (runtime / "dotnet/dotnet").is_file() and any(version.startswith("9.") for version in dotnet_versions),
                "dotnet_8": any(version.startswith("8.") for version in dotnet_versions),
                "dotnet_9": any(version.startswith("9.") for version in dotnet_versions),
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
