import requests
import json

# 1. Base URL for local KALKI AI Gateway
BASE_URL = "http://localhost:8000/api/v1"

def main():
    print("=== KALKI AI Gateway Integration Client ===")
    try:
        print("\n--- 1. Testing Chat & Agent completions endpoint ---")
        chat_payload = {
            "messages": [
                {"role": "user", "content": "Analyze KALKI agent protocols and security compliance."}
            ],
            "provider": "mock",
            "model": "kalki-mock-model",
            "use_rag": True,
            "enable_agents": True
        }
        response = requests.post(f"{BASE_URL}/chat/completions", json=chat_payload, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"Status: {data.get('status')}")
            print(f"Latency: {data.get('latency_ms')} ms")
            print(f"Response: {data.get('response')}")
        else:
            print(f"Status: {response.status_code} - {response.text}")

        print("\n--- 2. Uploading a custom document to RAG ---")
        upload_payload = {
            "title": "Quantum Lattice Keystone Security",
            "content": "KALKI AI implements custom zero-trust microservice encryption matching federal compliance standards."
        }
        upload_response = requests.post(f"{BASE_URL}/rag/documents/upload", data=upload_payload, timeout=5)
        print("Upload status:", upload_response.json())

        print("\n--- 3. Querying RAG vector store for the uploaded document ---")
        search_payload = {
            "query": "Quantum security",
            "top_k": 3
        }
        search_response = requests.post(f"{BASE_URL}/rag/search", json=search_payload, timeout=5)
        print("Search results:")
        print(json.dumps(search_response.json(), indent=2))
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
        print(f"\n[!] Note: FastAPI Gateway is not running at {BASE_URL}.")
        print("    To launch the backend server, run:")
        print("    python -m backend.app.main")
        print("    or double-click start_kalki.bat")

if __name__ == "__main__":
    main()
