import requests

url = 'http://127.0.0.1:9090/put/weather'
data = {'key': 'value'}
response = requests.post(url, json=data)

print('Status Code:', response.status_code)
print('Response Body:', response.text)