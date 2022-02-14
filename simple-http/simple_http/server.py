import os
from urllib.parse import urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    rootdir = os.path.abspath(os.curdir)
    mime_types = {
        '': 'octstream',
        '.json': 'application/json',
        '.html': 'text/html',
        '.htm': 'text/html',
        '.txt': 'text/plain',
        '.cpp': 'text/plain',
        '.md': 'text/plain',
        '.py': 'text/plain',
        '.go': 'text/plain',
        '.cc': 'text/plain',
        '.c': 'text/plain',
    }

    def do_GET(self):
        qres = urlparse(self.path)
        realpath = os.path.join(self.rootdir, qres.path.lstrip('/'))
        if not os.path.exists(realpath):
            return self.process_error(404, 'File "%s" not found' % realpath)
        if os.path.isdir(realpath):
            for index in ('index.html', 'index.htm'):
                index_file = os.path.join(realpath, index)
                if os.path.exists(index_file):
                    return self.process_file(index_file)
            return self.process_folder(realpath, self.path)
        return self.process_file(realpath)

    def process_folder(self, realpath, path):
        content = '<html><body><ul>'
        for subpath in os.listdir(realpath):
            lipath = os.path.join(path, subpath)
            if os.path.isdir(os.path.join(realpath, subpath)):
                subpath += '/'
            content += '<li><a href="%s">%s</a></li>' % (lipath, subpath)
        content += '</ul></body></html>'
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

    def process_file(self, realpath):
        _, ext = os.path.splitext(realpath)
        if ext in self.mime_types:
            mime_type = self.mime_types[ext]
        else:
            mime_type = self.mime_types['']
        with open(realpath, 'rb') as f:
            content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', mime_type)
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)

    def process_error(self, err, msg):
        self.send_error(err, msg)

class SimpleHTTPServer(HTTPServer):
    def __init__(self, server_address, rootdir=None):
        super().__init__(server_address, SimpleHTTPRequestHandler)
        if rootdir:
            SimpleHTTPRequestHandler.rootdir = os.path.abspath(rootdir)
