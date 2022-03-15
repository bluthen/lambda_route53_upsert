# About

Allows you to make a request to update a route 53 A record to the requesters IP address. Can be used as a dynamic dns 
replacement.

# Deploy
 1. cp settings.default.json settings.json
 2. edit settings.json with your info.
 3. export HOSTED_ZONE_ID=`cat settings.json |jq -r '.hosted_zone_id'`
 4. npm run deploy

# Usage

Make a post_payload.json file:

```
{"name": "your_domain_you_want_to_set", "password": "password that matches in settings.json"}
```

curl -i -k -d "@./post_payload.json" -X POST -H 'Content-Type: application/json' https://$LAMBDA_ENDPOINT/update_ddns