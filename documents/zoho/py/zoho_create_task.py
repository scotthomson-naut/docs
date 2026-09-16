import urllib.request
import urllib.error
import json

from zoho_auth import get_access_token


PORTAL_ID = "110003350473"
PROJECT_ID = "18662000000048092"
TASKLIST_ID = "18662000000047879"

ACCESS_TOKEN = get_access_token()

url = (
    f"https://projects.zohocloud.ca/api/v3/"
    f"portal/{PORTAL_ID}/projects/{PROJECT_ID}/tasks"
)

task_data = {
    "name": "API Test - UI Panel",
    "description": "Testing creation of a task directly in the UI Panel task list.",
    "tasklist": {
        "id": TASKLIST_ID
    }
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

        print("\nTASK CREATED")
        print("-" * 60)
        print("Task ID:   ", result.get("id"))
        print("Name:      ", result.get("name"))

        tasklist = result.get("tasklist", {})
        print("Task List: ", tasklist.get("name"))
        print("List ID:   ", tasklist.get("id"))

        print("\nFull response:")
        print(json.dumps(result, indent=4))

except urllib.error.HTTPError as error:
    print("HTTP Error:", error.code)
    print(error.read().decode("utf-8"))

except Exception as error:
    print("Error:", error)