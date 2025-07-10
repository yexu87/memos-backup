from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler

from urllib.parse import parse_qs, urlparse,  unquote
import json
import urllib

import requests
from requests.auth import HTTPBasicAuth

DA_HOST = 'https://server8.webhostmost.com:2222'
DA_LOGIN = 'username'
DA_PASS = 'password'
AUTH = HTTPBasicAuth(DA_LOGIN, DA_PASS)
HEADERS = {'Content-Type': 'application/json'}

class CustomHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print('path = {}'.format(self.path))
      
        parsed_path = urlparse(self.path)
        pq = parse_qs(parsed_path.query)
        print('parsed: path = {}, query = {}'.format(parsed_path.path, pq))

        action = ''
        command = ''
        select0 = ''
        id = ''
        
        if len(pq.get('action', [])) > 0 :
            action = pq.get('action', [])[0]

        if len(pq.get('command', [])) > 0 :
            command = pq.get('command', [])[0]

        if len(pq.get('select0', [])) > 0 :
            select0 = pq.get('select0', [])[0]

        if len(pq.get('id', [])) > 0 :
            id = pq.get('id', [])[0]

        print('query: action = {}, command = {}, select0 = {}, id = {}'.format(action, command, select0, id))
        
        if parsed_path.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Hello, world')
        elif parsed_path.path == '/job':
            try:
                if action == '' :
                    url = f"{DA_HOST}/CMD_CRON_JOBS?json=yes"
                    response = requests.get(url, auth=AUTH)
                    response.raise_for_status()
                    print(response.text)
                    
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(response.text.encode())
                    return
                    
                elif  action== 'create' :
                    if command == '' :
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(b'No command')
                        return

                    params = {}
                    params['reboot'] = 'no'
                    params['minute'] = '*'
                    params['hour'] = '*'
                    params['dayofmonth'] = '*'
                    params['month'] = '*'
                    params['dayofweek'] = '*'
                    params['command'] = command
                    params['json'] = 'yes'
                    params['action'] = 'create'

                    json_data = json.dumps(params)
                    print(params)
                    print(json_data)

                    url_post = f"{DA_HOST}/CMD_CRON_JOBS?json=yes"
                    response2 = requests.post(url_post, data=json_data, auth=AUTH, headers=HEADERS)
                    print(response2.text)
                    
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(response2.text.encode())
                    return

                elif  action== 'delete' :
                    if select0 == '' :
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(b'No select0')
                        return

                    params = {}
                    params['select0'] = select0
                    params['json'] = 'yes'
                    params['action'] = 'delete'
                    params['delete'] = 'yes'

                    json_data = json.dumps(params)
                    print(params)
                    print(json_data)

                    url_post = f"{DA_HOST}/CMD_CRON_JOBS?json=yes"
                    response2 = requests.post(url_post, data=json_data, auth=AUTH, headers=HEADERS)
                    print(response2.text)
                    
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(response2.text.encode())
                    return

                elif  action== 'save' :
                    if id == '' :
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(b'No id')
                        return

                    if command == '' :
                        self.send_response(200)
                        self.end_headers()
                        self.wfile.write(b'No command')
                        return

                    params = {}
                    params['id'] = id
                    params['minute'] = '*'
                    params['hour'] = '*'
                    params['dayofmonth'] = '*'
                    params['month'] = '*'
                    params['dayofweek'] = '*'
                    params['command'] = command
                    params['json'] = 'yes'
                    params['save'] = 'yes'

                    json_data = json.dumps(params)
                    print(params)
                    print(json_data)

                    url_post = f"{DA_HOST}/CMD_CRON_JOBS?json=yes"
                    response2 = requests.post(url_post, data=json_data, auth=AUTH, headers=HEADERS)
                    print(response2.text)
                    
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(response2.text.encode())
                    return

                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain; charset=utf-8')
                    self.end_headers()
                    self.wfile.write('action parameter wrong'.encode())
                    return

            except Exception as e:
                msg = 'error with build:{0}'.format(str(e))
                self.send_response(500)
                self.end_headers()
                self.wfile.write(msg.encode())
                return

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')

server_address = ('', 8080)
print("serving at port"， 8080)
httpd = HTTPServer(server_address, CustomHTTPRequestHandler)
httpd.serve_forever()
