#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess
import os

ALLOWED_COMMANDS = {
    "start_apache":   ["sudo", "/usr/bin/systemctl", "start",   "apache2"],
    "stop_apache":    ["sudo", "/usr/bin/systemctl", "stop",    "apache2"],
    "restart_apache": ["sudo", "/usr/bin/systemctl", "restart", "apache2"],
    "status_apache":  ["sudo", "/usr/bin/systemctl", "status",  "apache2", "--no-pager"],
}

class ControlHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        cmd_name = self.path.strip("/")
        if cmd_name not in ALLOWED_COMMANDS:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Comando no reconocido")
            return
        try:
            result = subprocess.run(
                ALLOWED_COMMANDS[cmd_name],
                capture_output=True, text=True, timeout=15
            )
            output = result.stdout + result.stderr
            if not output.strip():
                output = f"Ejecutado (exit code: {result.returncode})"
        except Exception as e:
            output = f"Error: {str(e)}"
        self.send_response(200)
        self.end_headers()
        self.wfile.write(output.encode())

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 9999), ControlHandler)
    print("Control server corriendo en puerto 9999")
    server.serve_forever()
