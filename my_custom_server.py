import json
from http.server import HTTPServer, BaseHTTPRequestHandler

profile_object = {
    'name': 'Sajad',
    'bio': '',
}


class CustomHandler(BaseHTTPRequestHandler):
    def _send_response(self, status, data):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_GET(self):
        if self.path == '/profile':
            self._send_response(200, profile_object)
        else:
            self._send_response(404, {'status': 'not found'})

    def do_PUT(self):
        if self.path == '/profile/update':
            content_length = int(self.headers['Content-Length'])
            request_body = self.rfile.read(content_length)
            print(f'Request body before json load: {request_body}')
            request_body = json.loads(request_body)
            print(f'Request body after json load: {request_body}')
            global profile_object
            profile_object = request_body
            self._send_response(200, {'status': 'success'})
        else:
            self._send_response(404, {'status': 'not found'})

    def do_PATCH(self):
        if self.path == '/profile/update/name':
            content_length = int(self.headers['Content-Length'])
            request_body = self.rfile.read(content_length)
            print(f'Request body before json load: {request_body}')
            request_body = json.loads(request_body)
            print(f'Request body after json load: {request_body}')
            global profile_object
            profile_object['name'] = request_body['name']
            self._send_response(200, {'status': 'success'})
        else:
            self._send_response(404, {'status': 'not found'})

PORT = 5000
addr = ('', PORT)
handler = CustomHandler
server = HTTPServer(addr, handler)
server.serve_forever()
