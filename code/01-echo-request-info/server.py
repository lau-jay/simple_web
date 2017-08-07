#!/usr/bin/env python3
# encoding: utf-8
# author: pyclearl

import http.server as BaseHTTPServer

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

    def do_GET(self):
        page = self.create_page()
        self.send_content(page)

    def create_page(self):
        values = {
            'date_time' : self.date_time_string(),
            'client_host' : self.client_address[0],
            'client_port' : self.client_address[1],
            'command' : self.command,
            'path' : self.path
        }
        page = self.Page.format(**values)
        # format don't work on bytes
        return bytes(page,'utf8')

    def send_content(self, Page):
        self.send_response(200)
        self.send_header("Content-Type","text/html")
        self.send_header("Content-Length", str(len(Page)))
        self.end_headers()
        self.wfile.write(Page)



if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = BaseHTTPServer.HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()
