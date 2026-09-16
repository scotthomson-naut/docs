# Python imports
import urllib.request
import urllib.error
import json

# Local imports
from zoho_auth import get_access_token


# Credentials
PORTAL_ID = "110003350473"
PROJECT_ID = "18662000000048092"
ACCESS_TOKEN = get_access_token()

url = (
    f"https://projects.zohocloud.ca/api/v3/"
    f"portal/{PORTAL_ID}/projects/{PROJECT_ID}/tasklists"
)

request = urllib.request.Request(
    url,
    headers={
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    },
    method="GET"
)

try:
    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

        print("Status:", response.status)
        print(json.dumps(result, indent=4))

except urllib.error.HTTPError as error:
    print("HTTP Error:", error.code)
    print(error.read().decode("utf-8"))

except Exception as error:
    print("Error:", error)