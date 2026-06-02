import requests
res = requests.post(
    "http://localhost:8000/api/v1/auth/register",
    headers={"Origin": "http://localhost"},
    json={"full_name": "Test User", "email": "test3@test.com", "password": "Test@123"}
)
print("Status:", res.status_code)
print("Headers:", dict(res.headers))
print("Body:", res.text)
