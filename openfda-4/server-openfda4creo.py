import http.server
import socketserver

# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 8014


# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()


        if self.path == "/":
            with open("search.html","r") as f:
                message = f.read()
                url = str(self.wfile.write(bytes(message, "utf8")))
                conn.request("GET", "/drug/label.json" + url, None, headers)
                r1 = conn.getresponse()
                drugs_raw = r1.read().decode("utf-8")
                conn.close()

        elif "search" in self.path:
            params = self.path.split("?")[1]
            drug = params.split("&")[0].split("=")[1]
            limit = params.split("&")[1].split("=")[1]
            url = str(self.wfile.write(bytes(drug + " " + limit, "utf8")))
            conn.request("GET", "/drug/label.json" + url, None, headers)
            r1 = conn.getresponse()
            drugs_raw = r1.read().decode("utf-8")
            conn.close()

        return


# Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
print("prueba")
try:
    httpd.serve_forever()
except KeyboardInterrupt:
        pass

httpd.server_close()
print("")
print("Server stopped!")


# https://github.com/joshmaker/simple-python-webserver/blob/master/server.py
