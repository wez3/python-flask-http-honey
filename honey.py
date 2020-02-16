#!/usr/bin/python3

from flask import Flask, request
import json, hashlib, time

app = Flask(__name__)
meth = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']

@app.route('/', defaults={'path': ''},  methods = meth)
@app.route('/<path:path>',  methods = meth)
def all_routes(path):
  dict = defaultActions(request)
  write(dict)
  return ''

def defaultActions(request):
  dict = {}
  dict = parseHeaders(request.headers, dict)
  dict['request_type'] = request.method
  dict['path'] = request.full_path
  dict['ip_address'] = request.remote_addr
  if request.method == 'POST':
    dict['body'] = request.get_data().decode('utf-8')
  dict['hash'] = hashlib.md5(json.dumps(dict).encode('utf-8')).hexdigest()
  dict['unix_timestamp'] = int(time.time())
  dict['readable_timestamp'] = time.ctime()
  return dict


def parseHeaders(headers, dict):
  for header in headers:
    dict[header[0]] = header[1]
  return dict

def write(logline):
  with open("webserver.log", "a") as file:
    file.write(json.dumps(logline))
    file.write("\r\n")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False)
