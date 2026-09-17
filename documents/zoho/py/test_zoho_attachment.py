import json
import mimetypes
import os
import uuid
import urllib.request
import urllib.error

from zoho_auth import get_access_token


PORTAL_ID = "110003350473"
BASE_URL = "https://projects.zohocloud.ca"

FILE_PATH = "zoho_attachment_test.txt"

# IMPORTANT:
# Replace this with the long API ID for AS8I-T84.
TASK_ID = "18662000000090007"


def upload_attachment(file_path):
    access_token = get_access_token()

    boundary = "----ScriptronautBoundary" + uuid.uuid4().hex

    filename = os.path.basename(file_path)
    content_type = (
        mimetypes.guess_type(filename)[0]
        or "application/octet-stream"
    )

    with open(file_path, "rb") as f:
        file_data = f.read()

    body = bytearray()

    # ---------------------------------------------------------
    # entity_type
    # ---------------------------------------------------------

    body.extend(f"--{boundary}\r\n".encode())
    body.extend(
        b'Content-Disposition: form-data; name="entity_type"\r\n\r\n'
    )
    body.extend(b"task\r\n")

    # ---------------------------------------------------------
    # entity_id
    # ---------------------------------------------------------

    body.extend(f"--{boundary}\r\n".encode())
    body.extend(
        b'Content-Disposition: form-data; name="entity_id"\r\n\r\n'
    )
    body.extend(TASK_ID.encode("utf-8"))
    body.extend(b"\r\n")

    # ---------------------------------------------------------
    # upload_file
    # ---------------------------------------------------------

    body.extend(f"--{boundary}\r\n".encode())
    body.extend(
        (
            'Content-Disposition: form-data; '
            f'name="upload_file"; filename="{filename}"\r\n'
        ).encode()
    )
    body.extend(
        f"Content-Type: {content_type}\r\n\r\n".encode()
    )

    body.extend(file_data)
    body.extend(b"\r\n")

    # ---------------------------------------------------------
    # Close multipart body
    # ---------------------------------------------------------

    body.extend(f"--{boundary}--\r\n".encode())

    # ---------------------------------------------------------
    # Request
    # ---------------------------------------------------------

    url = (
        f"{BASE_URL}/api/v3/portal/"
        f"{PORTAL_ID}/associate-attachments"
    )

    request = urllib.request.Request(
        url,
        data=bytes(body),
        method="POST",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
    )

    try:
        with urllib.request.urlopen(request) as response:
            text = response.read().decode("utf-8")

            print("HTTP:", response.status)

            if text:
                result = json.loads(text)
                print(json.dumps(result, indent=4))
                return result

    except urllib.error.HTTPError as error:
        text = error.read().decode("utf-8")

        print("\nZOHO HTTP ERROR")
        print("Status:", error.code)
        print(text)

        return None


upload_attachment(FILE_PATH)