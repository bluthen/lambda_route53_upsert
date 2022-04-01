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

Then you can run this curl command:

```
curl -i -d "@./post_payload.json" -X POST -H 'Content-Type: application/json' $LAMBDA_ENDPOINT/update_ddns
```

You can also just get your IP address:
```
curl $LAMBDA_ENDPOINT
```

## Unit test

With a good post_payload.json made and $LAMBDA_ENDPOINT set correctly.

```pipenv sync && pipenv run python main_test.py```

## Run Locally

If you have your AWS environment variables set you can run this locally.

1. pipenv sync
2. export FLAS_APP=main
3. pipenv run flask run
4. export LAMBDA_ENDPOINT=http://localhost:5000

# Let's Encrypt Authenticator

After deploy with the following in your settings.json and creating a TXT record for _acme-challenge.yourdomain in your route53:

```
[ 
  ... other entries...,
  {
    "domain": "_acme-challenge.yourdomain",
    "password": "yourpasswordyoumake",
    "hosted_zone_id": "yourhostedzone",
    "type": "TXT"
  }
]
```

You can then run the following:

```
LAMBDA_ENDPOINT=yourendpoint certbot certonly --manual --manual-auth-hook /path/to/le_authenticator.py \
  --preferred-challenges=dns -d yourdomain
```

Make sure le_authenticator.py has a copy of settings.json where it is at with at least the _acme-challenge.yourdomain TXT record entry in it.

certbot should set up an auto renew timer if it was successful.

**Note:** You may want to set `endpoint` variable in le_authenticator.py instead of using environment variable if lets encrypt uses it automatically as a hook.