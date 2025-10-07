import requests
import os
from dotenv import load_dotenv
load_dotenv()
ACCESS_TOKEN = os.getenv("ASANA_PAT")

#initial sync id
def fetch_init():
    RESOURCE_GID = "1211436899216107"  # your project or task GID

    url = f"https://app.asana.com/api/1.0/events?resource={RESOURCE_GID}"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    # Make the request directly
    response = requests.get(url, headers=headers)

    # Parse the full JSON
    data = response.json()
    print(data)

    return (data.get("sync"))

#later sync id
def fetch_latest(sync_token=None):
    RESOURCE_GID = "1211436899216107"  # your project or task GID

    url = f"https://app.asana.com/api/1.0/events"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    params = {"resource": RESOURCE_GID}
    if sync_token:
        params["sync"] = sync_token

    response = requests.get(url, headers=headers, params=params)

    # Parse the full JSON
    data = response.json()
    print(data)

    lst = []
    lst.append(data.get("sync"))
    lst.append(data.get("data"))
    return lst
