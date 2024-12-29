import requests

BASE_URL = "http://localhost:8998"

def send_query(query):
    response = requests.post(f"{BASE_URL}/query", json={"query": query})
    if response.ok:
        return response.json()
    return {"error": "Failed to fetch response"}

if __name__ == "__main__":
    print("Welcome to Moshi CLI Client!")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        result = send_query(user_input)
        print("Moshi:", result.get("response", "No response"))
