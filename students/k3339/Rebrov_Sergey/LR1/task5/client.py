import requests


def send_post_request(url, discipline, grade):
    post_data = {
        'discipline': discipline,
        'grade': grade
    }
    response = requests.post(url, data=post_data)
    print(response.text)


send_post_request('http://localhost:8080', 'Русский язык', 5)
