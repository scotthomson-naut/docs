import requests
import json

CLIENT_ID = "1000.2Y1EV5L4Z7E6ILVYUIM4CXLISNOVDM"
CLIENT_SECRET = "99a4aabb026606f15ea354114e8a16a0430f5ccb89"
AUTH_CODE = "1000.0ce35dac49cfb33238830d2fbe3f79bf.00c45ab2432cf1d7b9fadb6e8c4a6f14"

url = "https://accounts.zohocloud.ca/oauth/v2/token"

data = {
    "code": AUTH_CODE,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "grant_type": "authorization_code"
}

response = requests.post(url, data=data)

print("Status:", response.status_code)

try:
    print(json.dumps(response.json(), indent=4))
except Exception:
    print(response.text)