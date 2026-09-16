import urllib.request
import urllib.error
import json

from zoho_auth import get_access_token


PORTAL_ID = "110003350473"
PROJECT_ID = "18662000000048092"

ACCESS_TOKEN = get_access_token()

url = (
    f"https://projects.zohocloud.ca/api/v3/"
    f"portal/{PORTAL_ID}/projects/{PROJECT_ID}/tasks"
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

        #print("Status:", response.status)
        #print(json.dumps(result, indent=4))

        tasks = result.get("tasks", [])
        tasklists = {}

        for task in tasks:
            tasklist = task.get("tasklist")

            if tasklist:
                tasklist_id = tasklist.get("id")
                tasklist_name = tasklist.get("name")

                if tasklist_id:
                    tasklists[tasklist_id] = tasklist_name


        print("\nTASK LISTS")
        print("-" * 60)

        for tasklist_id, tasklist_name in sorted(
            tasklists.items(),
            key=lambda item: item[1].lower()
        ):
            print(f"{tasklist_name:<30} {tasklist_id}")

except urllib.error.HTTPError as error:
    print("HTTP Error:", error.code)
    print(error.read().decode("utf-8"))

except Exception as error:
    print("Error:", error)