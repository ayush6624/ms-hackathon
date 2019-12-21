import requests
import os

OAUTH_API = "https://outpost.mapmyindia.com/api/security/oauth/token"
client_id = os.environ.get("MAP_CLIENT_ID")
client_secret = os.environ.get("MAP_CLIENT_SECRET")


def request_token():
    param = {"grant_type": "client_credentials"}
    oauth_data = {
        "client_id": client_id, "client_secret": client_secret
    }

    r = requests.post(url=OAUTH_API, data=oauth_data, params=param)
    print(r.json())


if __name__ == "__main__":
    request_token()
