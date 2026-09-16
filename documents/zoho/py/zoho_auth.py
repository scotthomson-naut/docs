import urllib.request
import urllib.parse
import urllib.error
import json
import time

CLIENT_ID = "1000.2Y1EV5L4Z7E6ILVYUIM4CXLISNOVDM"
CLIENT_SECRET = "99a4aabb026606f15ea354114e8a16a0430f5ccb89"
REFRESH_TOKEN = "1000.3c32dcfc2737d0c0e3371661f647555a.25a8220c089bdd3ea3efb745d4bf0389"

ACCOUNTS_URL = "https://accounts.zohocloud.ca"


# ----------------------------------------------------------------------
# Access-token cache
# ----------------------------------------------------------------------

_access_token = None
_access_token_expires = 0


def get_access_token():

    global _access_token
    global _access_token_expires

    # --------------------------------------------------------------
    # Reuse existing token if it is still valid.
    #
    # Give ourselves a 60-second safety margin.
    # --------------------------------------------------------------

    if (
        _access_token
        and time.time() < (_access_token_expires - 60)
    ):
        return _access_token

    # --------------------------------------------------------------
    # Generate a new access token
    # --------------------------------------------------------------

    url = f"{ACCOUNTS_URL}/oauth/v2/token"

    data = urllib.parse.urlencode({
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
    }).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=data,
        method="POST",
    )

    try:

        with urllib.request.urlopen(request) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

            if "access_token" not in result:
                raise RuntimeError(
                    f"Zoho did not return an access token: {result}"
                )

            _access_token = result["access_token"]

            # Zoho normally returns expires_in = 3600.
            expires_in = int(
                result.get("expires_in", 3600)
            )

            _access_token_expires = (
                time.time() + expires_in
            )

            return _access_token

    except urllib.error.HTTPError as error:

        message = error.read().decode("utf-8")

        raise RuntimeError(
            f"Unable to refresh Zoho access token: "
            f"HTTP {error.code}: {message}"
        )


if __name__ == "__main__":

    token = get_access_token()

    print(
        "Successfully generated/retrieved "
        "a Zoho access token."
    )

    print(
        "Token:",
        token[:12] + "..."
    )