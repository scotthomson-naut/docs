import urllib.request
import urllib.error
import json

from zoho_auth import get_access_token

PORTAL_ID = "110003350473"
TASK_ID = "186620000000086001"

ACCESS_TOKEN = get_access_token()

url = (
    f"https://projects.zohocloud.ca/api/v3/"
    f"portal/{PORTAL_ID}/tasks/{TASK_ID}"
)

print("URL:")
print(url)

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

        print("\nStatus:", response.status)
        print(json.dumps(result, indent=4))

except urllib.error.HTTPError as error:
    print("\nHTTP Error:", error.code)
    print(error.read().decode("utf-8"))