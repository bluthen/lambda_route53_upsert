# About

Allows you to make a request to update a route 53 A record to the requesters IP address. Can be used as a dynamic dns 
replacement. Also allows you to set TXT value, for example if using [letsencrypt](https://letsencrypt.org).

# Deploy
 1. cp settings.default.json settings.json
 2. edit settings.json with your info.
 3. npm ci
 4. npx sls deploy
 5. ``` export LAMBDA_ENDPOINT=`npx sls info |grep ANY| head -n1 | awk '{print $3}'` ```

# Usage

Make a post_payload.json file:

```
[{"domain": "some.domain.com", "password": "password that matches in settings.json", "type": "A|TXT", "value": "value if txt type"}, ...]
```
Note: If you need multiple domains set you can add more domain/password pairs.

Then you can run this curl command:

```
curl -i -k -d "@./post_payload.json" -X POST -H 'Content-Type: application/json' $LAMBDA_ENDPOINT/update_ddns
```

You can also just get your IP address:
```
curl $LAMBDA_ENDPOINT
```

## Unit test

With a good post_payload.json made and $LAMBDA_ENDPOINT set correctly.

```pipenv sync && pipenv run python main_test.py```
