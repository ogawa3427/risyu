#!/usr/bin/env python3
"""Minimal static dev server with browser auto-reload.

Usage:
  python dev_server.py
  python dev_server.py --port 8080 --root .
"""

from __future__ import annotations

import argparse
import http.server
import os
import socketserver
import threading
import time
import urllib.request

from pathlib import Path
from typing import Dict, Iterable, Set, TextIO
from urllib.parse import unquote, urlparse


DEFAULT_EXTENSIONS = {
    ".html",
    ".css",
    ".js",
    ".json",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".ico",
    ".webp",
}

RELOAD_SNIPPET = (
    "<script>"
    "(function(){"
    "var es=new EventSource('/__reload');"
    "es.onmessage=function(e){if(e.data==='reload'){location.reload();}};"
    "es.onerror=function(){/* noop */};"
    "})();"
    "</script>"
)

clients_lock = threading.Lock()
clients: Set[TextIO] = set()


def iter_files(root: Path, extensions: Set[str]) -> Iterable[Path]:
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in {".git", "__pycache__", ".venv", "node_modules"}]
        for name in files:
            path = Path(base) / name
            if path.suffix.lower() in extensions:
                yield path


def snapshot(root: Path, extensions: Set[str]) -> Dict[Path, float]:
    snap: Dict[Path, float] = {}
    for p in iter_files(root, extensions):
        try:
            snap[p] = p.stat().st_mtime
        except FileNotFoundError:
            continue
    return snap


def notify_reload() -> None:
    dead: Set[TextIO] = set()
    with clients_lock:
        for wfile in clients:
            try:
                wfile.write(b"data: reload\n\n")
                wfile.flush()
            except Exception:
                dead.add(wfile)
        for wfile in dead:
            clients.discard(wfile)


def watch_changes(root: Path, extensions: Set[str], interval: float) -> None:
    last = snapshot(root, extensions)
    while True:
        time.sleep(interval)
        current = snapshot(root, extensions)
        if current != last:
            last = current
            notify_reload()


class ReloadingHandler(http.server.SimpleHTTPRequestHandler):
    server_version = "HotReloadHTTP/1.0"

    def __init__(self, *args, directory: str, **kwargs):
        self._directory = directory
        super().__init__(*args, directory=directory, **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/__reload":
            self._handle_reload_stream()
            return
        if parsed.path == "/api":
            self._handle_proxy("https://kurisyushien.org/api")
            return
        super().do_GET()

    def _handle_proxy(self, url: str) -> None:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (dev-proxy)"})
            with urllib.request.urlopen(req, timeout=20) as resp:
                body = resp.read()
                ct = resp.headers.get("Content-Type", "application/json")
            self.send_response(200)
            self.send_header("Content-Type", ct)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
        except Exception as exc:
            msg = str(exc).encode()
            self.send_response(502)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg)

    def _handle_reload_stream(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        with clients_lock:
            clients.add(self.wfile)
        try:
            # Keep connection alive.
            while True:
                time.sleep(15)
                self.wfile.write(b": ping\n\n")
                self.wfile.flush()
        except Exception:
            pass
        finally:
            with clients_lock:
                clients.discard(self.wfile)

    def send_head(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        if path.endswith(".html") or path == "/":
            return self._send_injected_html(path)
        return super().send_head()

    def _send_injected_html(self, path: str):
        rel = "index.html" if path in {"/", ""} else path.lstrip("/")
        target = Path(self._directory) / rel
        if not target.exists() or not target.is_file():
            return super().send_head()
        try:
            raw = target.read_bytes()
        except OSError:
            self.send_error(404, "File not found")
            return None
        content = raw.decode("utf-8", errors="replace")
        lower = content.lower()
        if "</body>" in lower:
            idx = lower.rfind("</body>")
            content = content[:idx] + RELOAD_SNIPPET + content[idx:]
        else:
            content += RELOAD_SNIPPET
        body = content.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.end_headers()
        return self._bytes_file(body)

    @staticmethod
    def _bytes_file(content: bytes):
        import io

        return io.BytesIO(content)


def main() -> None:
    parser = argparse.ArgumentParser(description="Static dev server with hot reload")
    parser.add_argument("--host", default="127.0.0.1", help="bind host (default: 127.0.0.1)")
    parser.add_argument("--port", default=5500, type=int, help="bind port (default: 5500)")
    parser.add_argument("--root", default=".", help="document root (default: current directory)")
    parser.add_argument(
        "--interval",
        default=0.5,
        type=float,
        help="file watch polling interval seconds (default: 0.5)",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"invalid --root: {root}")

    watcher = threading.Thread(
        target=watch_changes,
        args=(root, DEFAULT_EXTENSIONS, args.interval),
        daemon=True,
    )
    watcher.start()

    handler = lambda *h_args, **h_kwargs: ReloadingHandler(*h_args, directory=str(root), **h_kwargs)
    with socketserver.ThreadingTCPServer((args.host, args.port), handler) as httpd:
        httpd.allow_reuse_address = True
        print(f"serving: http://{args.host}:{args.port} (root={root})")
        httpd.serve_forever()


if __name__ == "__main__":
    main()
