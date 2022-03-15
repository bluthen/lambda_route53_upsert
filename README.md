# About

Allows you to make a request to update a route 53 A record to the requesters IP address. Can be used as a dynamic dns 
replacement.

# Deploy
 1. cp settings.default.json settings.json
 2. edit settings.json with your info.
 3. npx sls deploy
 4. ``` export LAMBDA_ENDPOINT=`npx sls info |grep ANY| head -n1 | awk '{print $3}'` ```

# Usage

Make a post_payload.json file:

```
{"your_domain_you_want_to_set": "password that matches in settings.json"}
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
