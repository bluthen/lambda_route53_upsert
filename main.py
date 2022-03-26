import boto3
from flask import Flask, request, jsonify
import json

client = boto3.client('route53')
with open('settings.json') as json_file:
    settings = json.load(json_file)

TTL = 60
DEFAULT_TYPE = 'A'

app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    """
    Returns requesters IP address as json. {"ip": "IP_ADDRESS"}
    """
    return jsonify({'ip': request.remote_addr}), 200


@app.route('/update_ddns', methods=['POST'])
def update_ddns():
    """
    Sets a DNS Record if matches with what is in settings.json. If A record sets to requestors IP, if TXT sets to given
    value.
    ---
    requestBody:
        description: JSON of records to set.
        required: true
        content:
            application/json:
                schema:
                    type: array
                    items:
                        type: object
                        properties:
                            domain:
                                type: string
                                required: true
                                description: Domain to set, must match an entry in settings.json
                            password:
                                type: string
                                required: true
                                description: Domain matching password, must match what is in settings.json
                            type:
                                type: string
                                required: true
                                description: 'A' or 'TXT'
                            value:
                                required: false
                                description: Required for TXT record
    response:
        200:
            description: Records set
        400:
            description: Request payload didn't match required values.
    """
    data = request.json
    ip = request.remote_addr
    for item in data:
        domain = item['domain']
        password = item['password']
        rtype = item['type']
        found = False
        for setting in settings:
            if setting['domain'] == domain and setting['type'] == rtype and setting['password'] == password:
                item['hosted_zone_id'] = setting['hosted_zone_id']
                found = True
                break
        if not found:
            return 'Invalid parameters', 400

    for item in data:
        domain = item['domain']
        rtype = item['type']
        hz = item['hosted_zone_id']
        if rtype == 'A':
            value = ip
        else:
            value = item['value']
        update = {
            "Comment": "Updated From DDNS Lambda",
            "Changes": [
                {
                    "Action": "UPSERT",
                    "ResourceRecordSet": {
                        "ResourceRecords": [
                            {
                                "Value": value
                            }
                        ],
                        "Name": domain,
                        "Type": rtype,
                        "TTL": TTL
                    }
                }
            ]
        }
        client.change_resource_record_sets(HostedZoneId=hz,
                                           ChangeBatch=update)
    return 'Okay', 200
