import urllib.parse
import urllib.request
import urllib.error

from zoho_auth import get_access_token

PORTAL_ID = "110003350473"
PROJECT_ID = "18662000000048092"
TASK_ID = "18662000000088016"
TAG_ID = "18662000000090016"

BASE_URL = "https://projects.zohocloud.ca"


def associate_tag():
    access_token = get_access_token()

    params = urllib.parse.urlencode({
        "tag_id": TAG_ID,
        "entity_id": TASK_ID,
        "entityType": "5",  # 5 = Task
    })

    url = (
        f"{BASE_URL}/api/v3/portal/{PORTAL_ID}"
        f"/projects/{PROJECT_ID}/tags/associate?{params}"
    )

    request = urllib.request.Request(
        url,
        method="POST",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    try:
        with urllib.request.urlopen(request) as response:
            text = response.read().decode("utf-8")

            print("HTTP:", response.status)

            if text:
                print(text)

    except urllib.error.HTTPError as error:
        text = error.read().decode("utf-8")

        print("\nZOHO HTTP ERROR")
        print("Status:", error.code)
        print(text)


associate_tag()