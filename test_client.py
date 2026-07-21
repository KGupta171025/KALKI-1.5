import requests
import json

# 1. Base URL for local KALKI AI Gateway
BASE_URL = "http://localhost:8000/api/v1"

print("--- 1. Testing Chat & Agent completions endpoint ---")
chat_payload = {
    "messages": [
        {"role": "user", "content": "Analyze KALKI agent protocols and security compliance."}
    ],
    "use_rag": True,
    "enable_agents": True
}
response = requests.post(f"{BASE_URL}/chat/completions", json=chat_payload)
if response.status_code == 200:
    data = response.json()
    print(f"Status: {data['status']}")
    print(f"Latency: {data['latency_ms']} ms")
    print(f"Response: {data['response']}")
else:
    print(f"Failed: {response.status_code} - {response.text}")

print("\n--- 2. Uploading a custom document to RAG ---")
upload_payload = {
    "title": "Quantum Lattice Keystone Security",
    "content": "KALKI AI implements custom zero-trust microservice encryption matching federal compliance standards."
}
upload_response = requests.post(f"{BASE_URL}/rag/documents/upload", data=upload_payload)
print("Upload status:", upload_response.json())

print("\n--- 3. Querying RAG vector store for the uploaded document ---")
search_payload = {
    "query": "Quantum security",
    "top_k": 3
}
search_response = requests.post(f"{BASE_URL}/rag/search", json=search_payload)
print("Search results:")
print(json.dumps(search_response.json(), indent=2))
