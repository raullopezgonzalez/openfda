# A basic web server using sockets


import socket

PORT = 8098
MAX_OPEN_REQUESTS = 5

def process_client(clientsocket):
    print(clientsocket)
    print("aqui")
    message = clientsocket.recv(1024)
    print(message)
    message = message.decode()
    message = message.split("\n")
    message = message[0]
    print(message)
    if message == "GET / HTTP/1.1\r"	:
        print("llega¡¡")
        with open("file.html","r") as f:
            file = f.read()
        web_contents = file
        print("1")
        web_headers = "HTTP/1.1 200"
        web_headers += "\n" + "Content-Type: text/html"
        web_headers += "\n" + "Content-Length: %i" % len(str.encode(web_contents))
        clientsocket.send(str.encode(web_headers + "\n\n" + web_contents))
        print("2")
        clientsocket.close()
    elif message == "GET /new HTTP/1.1\r" :
        with open("file_2.html","r") as f:
            file = f.read()
        web_contents = file
        print("3")
        web_headers = "HTTP/1.1 200"
        web_headers += "\n" + "Content-Type: text/html"
        web_headers += "\n" + "Content-Length: %i" % len(str.encode(web_contents))
        clientsocket.send(str.encode(web_headers + "\n\n" + web_contents))
        print("4")
        clientsocket.close()
    else:
        print("heeeeewyyyyeyeyey")


# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host, and a well-known port
hostname = socket.gethostname()
# Let's use better the local interface name
hostname = "10.10.106.97"
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

except socket.error as ex:         
    print("Problemas using port %i. Do you have permission?" % PORT)
    print(ex) 
