#!/usr/bin/python3
import requests
import os
import time
import json
import sys

domain = os.environ.get('CERTBOT_DOMAIN')
validation = os.environ.get('CERTBOT_VALIDATION')
endpoint = os.environ.get('LAMBDA_ENDPOINT')

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json'), 'r') as f:
    settings = json.load(f)
    for entry in settings:
        if entry['domain'] == '_acme-challenge.' + domain and entry['type'] == 'TXT':
            payload = entry.copy()
            payload['value'] = validation
            # print(json.dumps([payload]))
            r = requests.post(endpoint + '/update_ddns', data=json.dumps([payload]),
                              headers={'Content-type': 'application/json'}, timeout=31)
            if r.status_code != 200:
                print(r.text, file=sys.stderr)
                sys.exit(1)
            time.sleep(31)
            break
