import urllib.request
import urllib.parse
import json

url_from_user = "https://klippify-test-999.surge.sh/callback?code=HHammKbE6fGxkjyLQzON28AuRc9V1-tooWRwYpWirJ2_9quQcPtG9GdB6EnJalsMUhlLKhRmFcxvRlGKktgyTz1R9J6_BIwjYhGHryCXXo1GpDq7Gp39iMnLEX3tbaUZ5Vc1ZKwNEeok95dSFyntklQYaAG-iXa7Yrd2Sf9wjY2ixlPYVqx7Kpx6Wko4CojASMEaQtuinr_GquVjdmLrYF_R53FKsE041hOyVj1X1L70dBdQLEmMSc0DCk4%2Av%214920.e1&scopes=user.info.basic%2Cuser.info.profile%2Cuser.info.stats%2Cvideo.list%2Cvideo.publish&state=test"

parsed_url = urllib.parse.urlparse(url_from_user)
code = urllib.parse.parse_qs(parsed_url.query)['code'][0]

client_key = "sbawkrz4lc399y38a3"
client_secret = "yKztnG4ixhpTebKt65rTg6BwTnE3Ds7F"
redirect_uri = "https://klippify-test-999.surge.sh/callback"
code_verifier = "test_verifier_klippify_12345678901234567890"

url = "https://open.tiktokapis.com/v2/oauth/token/"
data = {
    "client_key": client_key,
    "client_secret": client_secret,
    "code": code,
    "grant_type": "authorization_code",
    "redirect_uri": redirect_uri,
    "code_verifier": code_verifier
}

encoded_data = urllib.parse.urlencode(data).encode('utf-8')
req = urllib.request.Request(url, data=encoded_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        with open("tiktok_tokens_final.json", "w") as f:
            json.dump(result, f, indent=2)
        print("SUCCESS")
except urllib.error.HTTPError as e:
    print("ERROR:", e.read().decode('utf-8'))
