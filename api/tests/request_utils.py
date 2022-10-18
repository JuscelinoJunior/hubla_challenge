import requests


def request_to_api(endpoint, file, method):
    if method == "POST":
        response = requests.post("http://127.0.0.1:5000" + endpoint, files=file)
    else:
        response = requests.get("http://127.0.0.1:5000" + endpoint)

    return response.json(), response.status_code
