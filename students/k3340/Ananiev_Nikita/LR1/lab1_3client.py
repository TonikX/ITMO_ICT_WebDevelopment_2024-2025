import http.client

host = 'localhost'
client_conn = http.client.HTTPConnection(host, 8888)
client_conn.request('GET', 'index.html')
serv_response = client_conn.getresponse()
print(serv_response.read().decode())
