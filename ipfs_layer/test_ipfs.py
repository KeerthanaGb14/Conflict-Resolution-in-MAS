from ipfs_layer.ipfs_client import upload_json

data = {
    "test": "Hello IPFS",
    "value": 123
}

cid = upload_json(data)

print("CID:", cid)
