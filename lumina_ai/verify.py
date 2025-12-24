import requests
import sys

BASE = "http://127.0.0.1:8000/api"

def run_test():
    print("Running verification...")
    session = requests.Session()

    # 1. Signup
    print("1. Signup")
    u, p = "testuser", "password123"
    try:
        r = session.post(f"{BASE}/signup/", json={"username": u, "password": p, "email": "test@example.com"})
        print(f"Signup: {r.status_code}")
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    # 2. Login
    print("2. Login")
    r = session.post(f"{BASE}/login/", json={"username": u, "password": p})
    if r.status_code != 200:
        print(f"Login failed: {r.text}")
        return
    tokens = r.json()
    access = tokens['access']
    headers = {"Authorization": f"Bearer {access}"}
    print("Login successful")

    # 3. Create Chat (implicitly done via message or explicit create)
    # Testing explicit create
    print("3. Create Chat")
    r = session.post(f"{BASE}/chats/", json={"title": "Test Chat"}, headers=headers)
    if r.status_code != 201:
        print(f"Create Chat failed: {r.text}")
        return
    chat_id = r.json()['id']
    print(f"Chat created: ID {chat_id}")

    # 4. Send Message
    print("4. Send Message")
    r = session.post(f"{BASE}/chats/{chat_id}/message/", json={"content": "Hello AI"}, headers=headers)
    if r.status_code != 200:
        print(f"Send Message failed: {r.text}")
        return
    ai_msg = r.json()
    print(f"AI Response: {ai_msg['content']}")

    # 5. List Chats
    print("5. List Chats")
    r = session.get(f"{BASE}/chats/", headers=headers)
    if r.status_code == 200:
        print(f"Chats: {len(r.json())}")
    
    print("Verification Complete.")

if __name__ == "__main__":
    run_test()
