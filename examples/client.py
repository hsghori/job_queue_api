import requests


# example script to demonstrate the API

post_data = {
    'url': 'http://api.hostip.info/get_html.php?ip=12.215.42.19',
}

response = requests.post(
    'http://0.0.0.0:8000/api/job/',
    json=post_data,
)
print(response.json())

response = requests.get(
    'http://0.0.0.0:8000/api/job/1/',
)
print(response.json())
