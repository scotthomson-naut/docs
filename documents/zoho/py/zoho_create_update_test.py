import urllib.request
import urllib.error
import json
from datetime import datetime, timezone

from zoho_auth import get_access_token


PORTAL_ID = "110003350473"
PROJECT_ID = "18662000000048092"
TASKLIST_ID = "18662000000047879"


BASE_URL = (
    f"https://projects.zohocloud.ca/api/v3/"
    f"portal/{PORTAL_ID}/projects/{PROJECT_ID}/tasks"
)


def api_request(url, method="GET", data=None):
    access_token = get_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    body = None

    if data is not None:
        body = json.dumps(data).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=body,
        headers=headers,
        method=method
    )

    try:
        with urllib.request.urlopen(request) as response:
            text = response.read().decode("utf-8")

            if text:
                return response.status, json.loads(text)

            return response.status, None

    except urllib.error.HTTPError as error:
        text = error.read().decode("utf-8")

        print("\nHTTP ERROR")
        print("Method:", method)
        print("URL:   ", url)
        print("Status:", error.code)
        print(text)

        return error.code, None


# ---------------------------------------------------------
# 1. CREATE TASK
# ---------------------------------------------------------

print("Creating test task...")

create_data = {
    "name": "API Create Update Test",
    "description": "Created for testing immediate task update.",
    "tasklist": {
        "id": TASKLIST_ID
    }
}

status, task = api_request(
    BASE_URL,
    method="POST",
    data=create_data
)

print("\nCREATE STATUS:", status)

if not task:
    raise SystemExit("Task creation failed.")

task_id = task.get("id")

print("Created Task ID:", task_id)
print("Created Name:   ", task.get("name"))

tasklist = task.get("tasklist", {})

print("Task List:      ", tasklist.get("name"))
print("Task List ID:   ", tasklist.get("id"))


# ---------------------------------------------------------
# 2. UPDATE EXACT TASK WE JUST CREATED
# ---------------------------------------------------------


update_url = f"{BASE_URL}/{task_id}"

print("\nAssigning task to Scot...")
print("Task Id")
print(task_id)
print("PATCH URL:")
print(update_url)


START_DATE = "2026-09-16"
DUE_DATE = "2026-09-18"

SCOT_ZUID = "110003353082"
IN_PROGRESS_STATUS_ID = "18662000000000362"


update_data = {
    "start_date": START_DATE,
    "end_date": DUE_DATE,
    "priority": "high",
    "status": {
        "id": IN_PROGRESS_STATUS_ID
    },
    "owners_and_work": {
        "owners": [
            {
                "zuid": SCOT_ZUID
            }
        ]
    },
}

status, updated_task = api_request(
    update_url,
    method="PATCH",
    data=update_data
)

print("\nUPDATE STATUS:", status)

if updated_task:
    print(json.dumps(updated_task, indent=4))