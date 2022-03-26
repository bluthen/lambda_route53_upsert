import unittest
import os
import requests
import json
import uuid


class TestLambda(unittest.TestCase):
    def test_getip(self):
        self.assertTrue('ip' in requests.get(os.environ.get('LAMBDA_ENDPOINT')).json())

    def test_validpassword(self):
        with open('post_payload.json') as f:
            d = json.load(f)
        r = requests.post(os.environ.get('LAMBDA_ENDPOINT') + '/update_ddns', json=d)
        self.assertEquals(r.status_code, 200)

    def test_invalidpassword(self):
        with open('post_payload.json') as f:
            d = json.load(f)
        for domain in d:
            domain['password'] = str(uuid.uuid4())
        r = requests.post(os.environ.get('LAMBDA_ENDPOINT') + '/update_ddns', json=d)
        self.assertEquals(r.status_code, 400)


if __name__ == '__main__':
    unittest.main()
