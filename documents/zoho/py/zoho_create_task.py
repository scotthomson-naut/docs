import urllib.request
import urllib.error
import json

ACCESS_TOKEN = "1000.39797936c02569815e75301aa04120f7.208b60f9bf46819fcb1d64be54292081"

PORTAL_ID = "110003350473"
PROJECT_ID = "18662000000048092"

url = (
    f"https://projects.zohocloud.ca/api/v3/"
    f"portal/{PORTAL_ID}/projects/{PROJECT_ID}/tasks"
)

task_data = {
    "name": "Scriptronaut API Test Task2",
    "description": "This task was created using the Zoho Projects API.",
    "priority": "high"
}

data = json.dumps(task_data).encode("utf-8")

request = urllib.request.Request(
    url,
    data=data,
    headers={
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    },
    method="POST"
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