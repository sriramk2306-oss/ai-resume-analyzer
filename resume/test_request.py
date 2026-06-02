import requests

print("🔥 Script started")

url = "http://127.0.0.1:5000/analyze"
file_path = "Nithyashreee.K-resume.pdf"

print("📂 Opening file...")

with open(file_path, "rb") as f:
    print("📡 Sending request...")
    response = requests.post(url, files={"resume": f})

print("✅ Got response")

print("Status code:", response.status_code)

try:
    print("Response JSON:", response.json())
except Exception as e:
    print("❌ Error parsing JSON:", e)
    print("Raw response:", response.text)