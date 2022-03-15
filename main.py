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
    print(data, settings)
    if data['password'] == settings[data['name']]:
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
                        "Name": data['name'],
                        "Type": TYPE,
                        "TTL": TTL
                    }
                }
            ]
        }
        response = client.change_resource_record_sets(HostedZoneId=settings['hosted_zone_id'],
                                                      ChangeBatch=update)
        return response['ChangeInfo']['Status'], 200
    else:
        return 'Unauthorized', 401
