"""Send a build notification to an ephemeral local-only SMTP sink."""
import os
from pathlib import Path
import smtplib
import socketserver
import sys
import threading


class Handler(socketserver.StreamRequestHandler):
    def handle(self):
        self.wfile.write(b'220 local-lab\r\n')
        while True:
            line = self.rfile.readline()
            if not line:
                return
            command = line.upper()
            if command.startswith(b'DATA'):
                self.wfile.write(b'354 End with dot\r\n')
                message = []
                while True:
                    line = self.rfile.readline()
                    if line in (b'.\r\n', b''):
                        break
                    message.append(line)
                target = Path('/out') / (
                    'notice-' + os.environ['BUILD_NUMBER'] + '.eml')
                target.write_bytes(b''.join(message))
                self.wfile.write(b'250 accepted\r\n')
            elif command.startswith(b'QUIT'):
                self.wfile.write(b'221 bye\r\n')
                return
            else:
                self.wfile.write(b'250 OK\r\n')


with socketserver.TCPServer(('127.0.0.1', 0), Handler) as server:
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    port = server.server_address[1]
    message = ('Subject: Build ' + os.environ['BUILD_NUMBER']
               + '\r\n\r\nExit status: ' + sys.argv[1])
    with smtplib.SMTP('127.0.0.1', port, timeout=5) as smtp:
        smtp.sendmail('jenkins@localhost', ['student@localhost'], message)
    server.shutdown()
print('LOCAL SMTP: notification captured, no external recipient')
