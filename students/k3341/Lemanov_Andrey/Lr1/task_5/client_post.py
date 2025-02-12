import requests


def send_post_request():
    url = 'http://localhost:8080'
    data = {
        'discipline': 'math',
        'grade': '5'
    }
    response = requests.post(url, data=data)
    print(response.text)


def get_grades():
    url = 'http://localhost:8080'
    response = requests.get(url)
    print(response.text)


if __name__ == '__main__':
    send_post_request()
    get_grades()
