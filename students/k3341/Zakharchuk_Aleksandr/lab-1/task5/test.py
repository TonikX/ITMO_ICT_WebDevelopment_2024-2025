import requests


for subject in ("math", "science", "english"):
    for grade in range(50, 101, 25):
        resp = requests.post("http://localhost:8080", data=str(grade), params={"subject":subject})
        print(resp)
