import requests
import json

IPFS_API_URL = "http://127.0.0.1:5001/api/v0/add"

IPFS_GATEWAY = "http://127.0.0.1:8080/ipfs/"


def fetch_json(cid: str) -> dict:
    url = IPFS_GATEWAY + cid
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch IPFS content: {response.text}")

    return response.json()

def upload_json(data: dict) -> str:
    """
    Uploads JSON data to IPFS.
    Returns CID string.
    """

    json_bytes = json.dumps(data, indent=2).encode("utf-8")

    files = {
        "file": ("explanation.json", json_bytes)
    }

    response = requests.post(IPFS_API_URL, files=files)

    if response.status_code != 200:
        raise Exception(f"IPFS upload failed: {response.text}")

    result = response.json()
    cid = result["Hash"]

    print("Uploaded to IPFS. CID:", cid)

    return cid
