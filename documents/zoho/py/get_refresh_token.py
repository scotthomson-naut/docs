import urllib.parse
import urllib.request
import json

CLIENT_ID = "1000.2Y1EV5L4Z7E6ILVYUIM4CXLISNOVDM"
CLIENT_SECRET = "99a4aabb026606f15ea354114e8a16a0430f5ccb89"
GRANT_CODE = "1000.cf83f854d888d4f170c4cfb5e5fb995b.e1c03524a68a0081c49db73a3dc87bec"

url = "https://accounts.zohocloud.ca/oauth/v2/token"

data = urllib.parse.urlencode({
    "grant_type": "authorization_code",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "code": GRANT_CODE,
}).encode("utf-8")

request = urllib.request.Request(url, data=data, method="POST")

with urllib.request.urlopen(request) as response:
    result = json.loads(response.read().decode("utf-8"))

print(json.dumps(result, indent=4))