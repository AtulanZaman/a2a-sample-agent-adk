import requests

payload = {
    "jsonrpc": "2.0",
    "method": "tasks/send",
    "id": "1",
    "params": {
        "id": "task-1",
        "message": {
            "role": "user",
            "parts": [{"type": "text", "text": "Reimburse me"}]
        },
        "acceptedOutputModes": ["text"],
        "sessionId": "mysession"
    }
}

response = requests.post("http://localhost:10002/", json=payload)
print(response.json())