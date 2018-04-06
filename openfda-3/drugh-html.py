# A basic web server using sockets

import http.server
import socketserver
import socket
import json

PORT = 8093
MAX_OPEN_REQUESTS = 5
IP = "localhost"
def process_client(clientsocket):
    import http.client

    headers = {'User-Agent': 'http-client'}

    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET", "/drug/label.json?limit=10", None, headers)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    repos_raw = r1.read().decode("utf-8")
    conn.close()

    repos = json.loads(repos_raw)

    list = []
    i = 0
    intro = "<ol>" + "\n"
    end = "</ol>" + "\n"

    while i < 10:
        if 'active_ingredient' in repos['results'][i]:
            list.append(repos['results'][i]['active_ingredient'][0])
            i += 1
        else:
            i += 1
            list.append("This index has no drug")

    with open("drug.html","w") as f:
        f.write(intro)
        for element in list:
            element_1 = "<li>" + element + "</li>" + "<\n>"
            f.write(element_1)
        f.write(end)



class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        with open("drug.html", "r") as f:
            message = f.read()
        self.wfile.write(bytes(message, "utf8"))
        print("File served!")
        return

Handler = testHTTPRequestHandler
httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
        pass

httpd.server_close()
print("")
print("Server stopped!")




# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host, and a well-known port
hostname = socket.gethostname()
# Let's use better the local interface name
hostname = "localhost"
try:
    serversocket.bind((hostname, PORT))
    # become a server socket
    # MAX_OPEN_REQUESTS connect requests before refusing outside connections
    serversocket.listen(MAX_OPEN_REQUESTS)

    while True:
        # accept connections from outside
        print ("Waiting for connections at %s %i" % (hostname, PORT))
        (clientsocket, address) = serversocket.accept()
        # now do something with the clientsocket
        # in this case, we'll pretend this is a non threaded server
        process_client(clientsocket)

except socket.error:
    print("Problemas using port %i. Do you have permission?" % PORT)
