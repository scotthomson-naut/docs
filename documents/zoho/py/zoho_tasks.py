import urllib.request
import urllib.error
import urllib.parse
import json

from zoho_auth import get_access_token


# ----------------------------------------------------------------------
# Zoho configuration
# ----------------------------------------------------------------------

PORTAL_ID = "110003350473"
PROJECT_ID = "18662000000048092"

BASE_URL = "https://projects.zohocloud.ca/api/v3"

PROJECT_URL = (
    f"{BASE_URL}/portal/{PORTAL_ID}/projects/{PROJECT_ID}"
)

TASKS_URL = f"{PROJECT_URL}/tasks"


# ----------------------------------------------------------------------
# Known project users
#
# IMPORTANT:
# These are Zoho User IDs (ZUID), not the longer Zoho Projects user IDs.
# ----------------------------------------------------------------------

USERS = {
    "Scot Thomson": "110003353082",
    "Stéphane Barbin": "110003336135",
}


# ----------------------------------------------------------------------
# Known task lists
#
# We are keeping these here for now because the V3 task-list endpoint
# gave us the OAuth-scope problem.
# ----------------------------------------------------------------------

TASKLISTS = {
    "UI Panel": "18662000000047879",
    "General": "186620000000081029",
    "Animation": "186620000000048166",
}


# ----------------------------------------------------------------------
# Generic API request
# ----------------------------------------------------------------------

def api_request(url, method="GET", data=None):

    access_token = get_access_token()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    body = None

    if data is not None:
        body = json.dumps(data).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=body,
        headers=headers,
        method=method,
    )

    try:
        with urllib.request.urlopen(request) as response:
            text = response.read().decode("utf-8")
            if text:
                return response.status, json.loads(text)
            return response.status, None

    except urllib.error.HTTPError as error:

        text = error.read().decode("utf-8")

        print("\nZOHO HTTP ERROR")
        print("Method:", method)
        print("URL:   ", url)
        print("Status:", error.code)
        print(text)

        return error.code, None


# ----------------------------------------------------------------------
# Statuses
# ----------------------------------------------------------------------

def get_task_statuses():

    url = (
        f"{BASE_URL}/portal/{PORTAL_ID}/settings/global-statuses"
        f"?module=tasks"
    )

    status_code, result = api_request(url)

    if status_code != 200 or not result:
        return {}

    statuses = {}

    for status in result:
        name = status.get("name")
        status_id = status.get("id")

        if name and status_id:
            statuses[name.lower()] = status_id

    return statuses


def get_status_id(status_name):

    statuses = get_task_statuses()

    status_id = statuses.get(status_name.lower())

    if not status_id:
        raise ValueError(
            f"Unknown Zoho task status: {status_name}"
        )

    return status_id


# ----------------------------------------------------------------------
# Task-list lookup
# ----------------------------------------------------------------------

def get_tasklist_id(tasklist_name):

    tasklist_id = TASKLISTS.get(tasklist_name)

    if not tasklist_id:
        raise ValueError(
            f"Unknown Zoho task list: {tasklist_name}"
        )

    return tasklist_id


# ----------------------------------------------------------------------
# User lookup
# ----------------------------------------------------------------------

def get_user_zuid(user_name):

    zuid = USERS.get(user_name)

    if not zuid:
        raise ValueError(
            f"Unknown Zoho user: {user_name}"
        )

    return zuid


# ----------------------------------------------------------------------
# Create task
# ----------------------------------------------------------------------

def create_task(
    name,
    tasklist=None,
    owner=None,
    priority=None,
    status=None,
    start_date=None,
    due_date=None,
    description=None,
):

    # --------------------------------------------------------------
    # CREATE payload
    # --------------------------------------------------------------

    create_data = {
        "name": name
    }

    if description:
        create_data["description"] = description

    if tasklist:
        tasklist_id = get_tasklist_id(tasklist)
        create_data["tasklist"] = {
            "id": tasklist_id
        }

    print("\nCreating Zoho task...")
    print("Name:     ", name)

    if tasklist:
        print("Task List:", tasklist)

    create_status, task = api_request(
        TASKS_URL,
        method="POST",
        data=create_data,
    )

    if create_status != 201 or not task:
        print("\nTask creation failed.")
        return None

    task_id = str(task["id"])

    print("\nTask created.")
    print("Task ID:", task_id)

    # --------------------------------------------------------------
    # UPDATE payload
    #
    # Some fields have proven more reliable when PATCHed after the
    # task has been created.
    # --------------------------------------------------------------

    update_data = {}

    # Priority
    if priority:
        priority = priority.lower()
        valid_priorities = {
            "none",
            "low",
            "medium",
            "high",
        }

        if priority not in valid_priorities:
            raise ValueError(
                f"Invalid priority: {priority}"
            )

        update_data["priority"] = priority

    # Status
    if status:
        status_id = get_status_id(status)
        update_data["status"] = {
            "id": status_id
        }

    # Owner
    if owner:
        zuid = get_user_zuid(owner)
        update_data["owners_and_work"] = {
            "owners": [
                {
                    "zuid": zuid
                }
            ]
        }

    # Start Date
    if start_date:
        update_data["start_date"] = start_date

    # Due Date
    if due_date:
        update_data["end_date"] = due_date

    # --------------------------------------------------------------
    # PATCH task if required
    # --------------------------------------------------------------

    if update_data:
        task_url = f"{TASKS_URL}/{task_id}"
        print("\nUpdating task...")
        update_status, updated_task = api_request(
            task_url,
            method="PATCH",
            data=update_data,
        )

        if update_status != 200:
            print("\nTask was created, but update failed.")
            print("Task ID:", task_id)

            return task

        if updated_task:
            task = updated_task

        print("Task updated.")

    return task


# ----------------------------------------------------------------------
# Test
# ----------------------------------------------------------------------

if __name__ == "__main__":

    task = create_task(
        name="Reusable API Function Test",
        tasklist="UI Panel",
        owner="Scot Thomson",
        priority="high",
        status="In Progress",
        start_date="2026-09-16",
        due_date="2026-09-18",
        description="Created using the reusable zoho_tasks module.",
    )

    if task:
        print("\n" + "=" * 70)
        print("SUCCESS")
        print("=" * 70)

        print("Task ID: ", task.get("id"))
        print("Name:    ", task.get("name"))
        print("Priority:", task.get("priority"))
        print("Status:  ", task.get("status"))
        print("Start:   ", task.get("start_date"))
        print("Due:     ", task.get("end_date"))