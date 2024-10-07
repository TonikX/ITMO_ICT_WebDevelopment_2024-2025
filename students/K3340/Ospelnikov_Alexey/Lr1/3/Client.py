import http.client

host = 'localhost'
client_conn = http.client.HTTPConnection(host, 8080)
client_conn.request('GET', 'index.html')
response = client_conn.getresponse()
print(response.read().decode())