import boto3
from flask import Flask, request, jsonify
import json

client = boto3.client('route53')
with open('settings.json') as json_file:
    settings = json.load(json_file)

TTL = 60
TYPE = 'A'

app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    return jsonify({'ip': request.remote_addr}), 200


@app.route('/update_ddns', methods=['POST'])
def update_ddns():
    data = request.json
    ip = request.remote_addr
    for item in data.items():
        domain = item[0]
        password = item[1]
        if password != settings[domain]['password']:
            return 'Unauthorized', 401
    for item in data.items():
        domain = item[0]
        update = {
            "Comment": "Updated From DDNS Lambda",
            "Changes": [
                {
                    "Action": "UPSERT",
                    "ResourceRecordSet": {
                        "ResourceRecords": [
                            {
                                "Value": ip
                            }
                        ],
                        "Name": domain,
                        "Type": TYPE,
                        "TTL": TTL
                    }
                }
            ]
        }
        client.change_resource_record_sets(HostedZoneId=settings[domain]['hosted_zone_id'],
                                           ChangeBatch=update)
    return 'Okay', 200
