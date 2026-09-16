# Python imports
import sys
import urllib.request
import urllib.error
import urllib.parse
import json

# Local imports
from zoho_auth import get_access_token

sys.stdout.reconfigure(encoding="utf-8")

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

TASKLIST_FALLBACKS = {
    "general": "186620000000081029",
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
    """
    """
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
    """
    """
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
    """
    """
    statuses = get_task_statuses()
    status_id = statuses.get(status_name.lower())

    if not status_id:
        raise ValueError(
            f"Unknown Zoho task status: {status_name}"
        )

    return status_id


# ----------------------------------------------------------------------
# Lookup Functions
# ----------------------------------------------------------------------

def get_tasks():
    """
    """
    tasks = []
    page = 1

    while True:
        url = f"{TASKS_URL}?page={page}&per_page=100"
        status_code, result = api_request(url)

        if status_code != 200 or not result:
            raise RuntimeError(
                "Unable to retrieve Zoho project tasks."
            )

        tasks.extend(result.get("tasks", []))

        page_info = result.get("page_info", {})

        if not page_info.get("has_next_page"):
            break

        page += 1

    return tasks


def get_task(task_id):
    """
    """
    url = f"{TASKS_URL}/{task_id}"
    status_code, task = api_request(url)
    if status_code != 200 or not task:
        raise RuntimeError(
            f"Unable to retrieve Zoho task: {task_id}"
        )

    return task


def get_tasklist_id(tasklist_name, tasklists=None):
    """
    """
    if tasklists is None:
        tasklists = get_project_tasklists()

    key = tasklist_name.lower()

    # First try dynamically discovered Task Lists
    tasklist = tasklists.get(key)

    if tasklist:
        return tasklist["id"]

    # Fall back only when the list cannot be discovered through tasks
    fallback_id = TASKLIST_FALLBACKS.get(key)

    if fallback_id:
        return fallback_id

    available = [
        info["name"]
        for info in tasklists.values()
    ]

    raise ValueError(
        f"Unknown Zoho task list: {tasklist_name}\n"
        f"Available task lists: {', '.join(available)}"
    )


def update_task(
    task_id,
    name=None,
    owner=None,
    priority=None,
    status=None,
    start_date=None,
    due_date=None,
    description=None,
):
    """
    """
    update_data = {}

    # Name
    if name is not None:
        update_data["name"] = name

    # Description
    if description is not None:
        update_data["description"] = description

    # Priority
    if priority is not None:
        update_data["priority"] = priority.lower()

    # Status
    if status is not None:
        status_id = get_status_id(status)
        update_data["status"] = {
            "id": status_id
        }

    # Owner
    if owner is not None:
        zuid = get_user_zuid(owner)
        update_data["owners_and_work"] = {
            "owners": [
                {
                    "zuid": zuid
                }
            ]
        }

    # Start Date
    if start_date is not None:
        update_data["start_date"] = start_date

    # Due Date
    if due_date is not None:
        update_data["end_date"] = due_date

    if not update_data:
        raise ValueError(
            "No task properties were supplied to update."
        )

    url = f"{TASKS_URL}/{task_id}"

    print("\nUpdating Zoho task...")
    print("Task ID:", task_id)

    status_code, task = api_request(
        url,
        method="PATCH",
        data=update_data,
    )

    if status_code != 200 or not task:
        raise RuntimeError(
            f"Unable to update Zoho task: {task_id}"
        )

    print("Task updated.")

    return task


# ----------------------------------------------------------------------
# Find tasks
# ----------------------------------------------------------------------

def find_tasks(
    name=None,
    tasklist=None,
    status=None,
    owner=None,
):
    """
    """
    tasks = get_tasks()
    matches = []
    for task in tasks:
        # ----------------------------------------------------------
        # Name
        # ----------------------------------------------------------

        if name is not None:
            task_name = task.get("name", "")
            if task_name.lower() != name.lower():
                continue

        # ----------------------------------------------------------
        # Task List
        # ----------------------------------------------------------

        if tasklist is not None:

            tasklist_data = task.get("tasklist") or {}
            tasklist_name = tasklist_data.get("name", "")

            if tasklist_name.lower() != tasklist.lower():
                continue

        # ----------------------------------------------------------
        # Status
        # ----------------------------------------------------------

        if status is not None:
            status_data = task.get("status") or {}
            status_name = status_data.get("name", "")

            if status_name.lower() != status.lower():
                continue

        # ----------------------------------------------------------
        # Owner
        # ----------------------------------------------------------

        if owner is not None:
            owners = task.get("owners") or []
            owner_found = False

            for task_owner in owners:
                owner_name = (
                    task_owner.get("full_name")
                    or task_owner.get("name")
                    or ""
                )

                if owner_name.lower() == owner.lower():
                    owner_found = True
                    break

            if not owner_found:
                continue

        matches.append(task)

    return matches


def find_task(name, tasklist=None):
    """
    """
    matches = find_tasks(
        name=name,
        tasklist=tasklist,
    )

    if not matches:
        return None

    if len(matches) > 1:
        raise ValueError(
            f"More than one task named '{name}' was found. "
            f"Specify a task list to narrow the search."
        )

    return matches[0]


def delete_task(task_id):
    """
    """
    url = f"{TASKS_URL}/{task_id}"

    print("\nDeleting Zoho task...")
    print("Task ID:", task_id)

    status_code, result = api_request(
        url,
        method="DELETE",
    )

    # Zoho may return 200 or 204 depending on the response.
    if status_code not in (200, 204):
        raise RuntimeError(
            f"Unable to delete Zoho task: {task_id}"
        )

    print("Task deleted.")

    return True


def get_project_tasklists():
    """
    """
    tasklists = {}
    page = 1

    while True:
        url = f"{TASKS_URL}?page={page}&per_page=100"

        status_code, result = api_request(url)

        if status_code != 200 or not result:
            raise RuntimeError(
                "Unable to retrieve Zoho project tasks."
            )

        tasks = result.get("tasks", [])

        for task in tasks:
            tasklist = task.get("tasklist")

            if not isinstance(tasklist, dict):
                continue

            name = tasklist.get("name")
            tasklist_id = tasklist.get("id")

            if name and tasklist_id:
                tasklists[name.lower()] = {
                    "name": name,
                    "id": str(tasklist_id),
                }

        page_info = result.get("page_info", {})

        if not page_info.get("has_next_page"):
            break

        page += 1

    return tasklists


def get_user_zuid(user_name):
    """
    """
    zuid = USERS.get(user_name)

    if not zuid:
        raise ValueError(
            f"Unknown Zoho user: {user_name}"
        )

    return zuid


def get_project_users():
    """
    """
    url = f"{PROJECT_URL}/users"

    status_code, result = api_request(url)

    if status_code != 200 or not result:
        raise RuntimeError(
            "Unable to retrieve Zoho project users."
        )

    users = {}
    for user in result.get("users", []):
        name = user.get("full_name")
        zuid = user.get("zuid")

        if name and zuid:
            users[name.lower()] = {
                "name": name,
                "zuid": str(zuid),
                "project_user_id": str(user.get("id", "")),
                "email": user.get("email", ""),
            }

    return users


def get_user_zuid(user_name):
    """
    """
    users = get_project_users()
    user = users.get(user_name.lower())

    if not user:
        available = [
            info["name"]
            for info in users.values()
        ]

        raise ValueError(
            f"Unknown Zoho project user: {user_name}\n"
            f"Available users: {', '.join(available)}"
        )

    return user["zuid"]


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
    """
    """

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

    print("\nFIND DELETE TEST TASK")
    print("=" * 70)

    task = find_task(
        "API Delete Test",
        tasklist="UI Panel",
    )

    if task:

        print("Found!")
        print("Name:   ", task.get("name"))
        print("Task ID:", task.get("id"))
        print("Task Key:   ", task.get("prefix"))

        print("\nFULL TASK")
        print(json.dumps(task, indent=4))

    else:
        print("API Delete Test was not found.")