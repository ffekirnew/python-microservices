import requests


def login(username: str, password: str) -> dict[str, str]:
    response = requests.post(
        "http://localhost:8000/login", json={"username": username, "password": password}
    )

    if response.status_code != 200:
        raise Exception("Invalid credentials")

    return response.json()


def authenticate(token: str) -> dict[str, str]:
    response = requests.post(
        "http://localhost:8000/authenticate",
        headers={"Authorization": f"Bearer {token}"},
    )

    if response.status_code != 200:
        raise Exception("Unauthorized")

    return response.json()
