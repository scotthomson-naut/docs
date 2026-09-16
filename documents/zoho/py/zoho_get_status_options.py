import urllib.request
import urllib.error
import json

from zoho_auth import get_access_token


PORTAL_ID = "110003350473"

ACCESS_TOKEN = get_access_token()

url = (
    f"https://projects.zohocloud.ca/api/v3/"
    f"portal/{PORTAL_ID}/settings/global-statuses"
    f"?module=tasks"
)

print("Getting Zoho Task statuses...")
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
        text = response.read().decode("utf-8")
        result = json.loads(text)

        print("\nSTATUS:", response.status)

        print("\nTASK STATUSES")
        print("-" * 70)

        for status in result:
            print(
                f"{status.get('name', ''):<25} "
                f"ID: {status.get('id', '')}"
            )

        print("\nFULL RESPONSE")
        print("-" * 70)
        print(json.dumps(result, indent=4))

except urllib.error.HTTPError as error:
    print("\nHTTP ERROR")
    print("Status:", error.code)
    print(error.read().decode("utf-8"))

except Exception as error:
    print("\nERROR:")
    print(error)