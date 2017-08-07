#!/usr/bin/env python3
# encoding: utf-8
# author: pyclearl

import sys, os
import http.server as BaseHTTPServer




class ServerException(Exception):
    '''
    服务器内部错误
    '''
    pass

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    '''
    处理请求并返回页面
    '''
    Page = '''
        <html>
        <body>
           <table>
              <tr><td>Header</td><td>Value</td></tr>
              <tr><td>Date and time</td><td>{date_time}</td></tr>
              <tr><td>Client host</td><td>{client_host}</td></tr>
              <tr><td>Client port</td><td>{client_port}</td></tr>
              <tr><td>Command</td><td>{command}</td></tr>
              <tr><td>Path</td><td>{path}</td></tr>
           </table>
        </body>
        </html>
        '''
    Error_Page = """
    <html>
        <body>
            <h1>Error accessing {path}</h1>
            <p>{msg}</p>
        </body>
    </html>
    """

    def do_GET(self):
        try:
            full_path = os.getcwd() + self.path
            if not os.path.exists(full_path):
                raise ServerException("'{0}' not found".format(self.path))
            elif os.path.isfile(full_path):
                self.handle_file(full_path)
            else:
                raise ServerException("Unknown object '{0}'".format(self.path))
        except Exception as msg:
            self.handle_error(msg)

    def handle_file(self, full_path):
        try:
            with open(full_path, 'rb') as reader:
                content = reader.read()
            self.send_content(content)
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(self.path, msg)
            self.handle_error(msg)

    def handle_error(self, msg):
        content = bytes(self.Error_Page.format(path=self.path, msg=msg), 'utf8')
        self.send_content(content)

    def send_content(self, Page):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Content-Length", str(len(Page)))
        self.end_headers()
        self.wfile.write(Page)



if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = BaseHTTPServer.HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()
