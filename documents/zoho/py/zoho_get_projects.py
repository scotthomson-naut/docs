import urllib.request
import urllib.error
import json

ACCESS_TOKEN = "1000.39797936c02569815e75301aa04120f7.208b60f9bf46819fcb1d64be54292081"
PORTAL_ID = "110003350473"

url = (
    f"https://projects.zohocloud.ca/api/v3/"
    f"portal/{PORTAL_ID}/projects"
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