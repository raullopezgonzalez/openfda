import http.server
import socketserver
import json
import http.client
import socket

# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 8000
socketserver.TCPServer.allow_reuse_adress = True


# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):


        intro = "<!doctype html>" + "\n" + "<html>" + "\n" + "<body>" + "\n" "<ul>" + "\n"
        end = "</ul>" + "\n" + "</body>" + "\n" + "</html>"

        try:
            if self.path == "/":
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open("search.html", "r") as f:
                    message = f.read()
                    self.wfile.write(bytes(message, "utf8"))

            elif "searchDrug" in self.path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                list=[]
                headers = {'User-Agent': 'http-client'}
                conn = http.client.HTTPSConnection("api.fda.gov")
                params = self.path.split("?")[1]
                drug = params.split("&")[0].split("=")[1]
                limit = params.split("&")[1].split("=")[1]
                url = "/drug/label.json?search=active_ingredient:" + drug + "&" + "limit=" + limit
                conn.request("GET", url, None, headers)
                r1 = conn.getresponse()
                drugs_raw = r1.read().decode("utf-8")
                conn.close()
                drug = json.loads(drugs_raw)
                drugs_1 = drug

                for i in range(len(drugs_1['results'])):
                    if 'active_ingredient' in drugs_1['results'][i]:
                        list.append(drugs_1['results'][i]['active_ingredient'][0])
                    else:
                        list.append("This index has no drug")
                with open("drug.html", "w") as f:
                    f.write(intro)
                    for element in list:
                        element_1 = "<li>" + element + "</li>" + "\n"
                        f.write(element_1)
                    f.write(end)
                with open("drug.html", "r") as f:
                    file = f.read()

                self.wfile.write(bytes(file, "utf8"))

            elif "searchCompanies" in self.path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                list=[]
                headers = {'User-Agent': 'http-client'}
                conn = http.client.HTTPSConnection("api.fda.gov")
                companies = self.path.split("?")[1]
                url = "/drug/label.json?search=manufacturer_name:" + companies
                conn.request("GET", url, None, headers)
                r1 = conn.getresponse()
                company_raw = r1.read().decode("utf-8")
                conn.close()
                companies = json.loads(company_raw)
                companies_1 = companies

                for i in range(len(companies_1['results'])):
                    if 'active_ingredient' in companies_1['results'][i]:
                        list.append(companies_1['results'][i]['openfda']["manufacturer_name"][0])
                    else:
                        list.append("This index has no manufacturer name")
                with open("drug.html", "w") as f:
                    f.write(intro)
                    for element in list:
                        element_1 = "<li>" + element + "</li>" + "\n"
                        f.write(element_1)
                    f.write(end)
                with open("drug.html", "r") as f:
                    file = f.read()

                self.wfile.write(bytes(file, "utf8"))

            elif "listDrugs" in self.path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                list=[]
                headers = {'User-Agent': 'http-client'}
                conn = http.client.HTTPSConnection("api.fda.gov")
                params = self.path.split("?")[1]
                drug = params.split("&")[0].split("=")[1]
                limit = params.split("&")[1].split("=")[1]
                url = "/drug/label.json?" + drug + "&" + "limit=" + limit
                conn.request("GET", url, None, headers)
                r1 = conn.getresponse()
                drugs_raw = r1.read().decode("utf-8")
                conn.close()
                drug = json.loads(drugs_raw)
                drugs_1 = drug

                for i in range(len(drugs_1['results'])):
                    if "openfda" in drugs_1["results"][i]:
                        list.append(drugs_1['results'][i]['openfda']["brand_name"][0])
                with open("drug.html", "w") as f:
                    f.write(intro)
                    for element in list:
                        element_1 = "<li>" + element + "</li>" + "\n"
                        f.write(element_1)
                    f.write(end)
                with open("drug.html", "r") as f:
                    file = f.read()

                self.wfile.write(bytes(file, "utf8"))

            elif "listCompanies" in self.path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                list = []
                headers = {'User-Agent': 'http-client'}
                conn = http.client.HTTPSConnection("api.fda.gov")
                drug = self.path.split("?")[1]
                url = "/drug/label.json?" + drug
                conn.request("GET", url, None, headers)
                r1 = conn.getresponse()
                drugs_raw = r1.read().decode("utf-8")
                conn.close()
                drug = json.loads(drugs_raw)
                drugs_1 = drug

                for i in range(len(drugs_1['results'])):
                    if "openfda" in drugs_1["results"][i]:
                        list.append(drugs_1['results'][i]['openfda']["manufacturer_name"][0])
                    else:
                        list.append("Unknow")

                with open("drug.html", "w") as f:
                    f.write(intro)
                    for element in list:
                        element_1 = "<li>" + element + "</li>" + "\n"
                        f.write(element_1)
                    f.write(end)
                with open("drug.html", "r") as f:
                    file = f.read()

                self.wfile.write(bytes(file, "utf8"))
            elif "listWarnings" in self.path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                list = []
                headers = {'User-Agent': 'http-client'}
                conn = http.client.HTTPSConnection("api.fda.gov")
                drug = self.path.split("?")[1]
                url = "/drug/label.json?" + drug
                conn.request("GET", url, None, headers)
                r1 = conn.getresponse()
                drugs_raw = r1.read().decode("utf-8")
                conn.close()
                drug = json.loads(drugs_raw)
                drugs_1 = drug

                for i in range(len(drugs_1['results'])):
                    if "openfda" in drugs_1["results"][i]:
                        list.append(drugs_1['results'][i]['warnings'][0])

                with open("drug.html", "w") as f:
                    f.write(intro)
                    for element in list:
                        element_1 = "<li>" + element + "</li>" + "\n"
                        f.write(element_1)
                    f.write(end)
                with open("drug.html", "r") as f:
                    file = f.read()

                self.wfile.write(bytes(file, "utf8"))

            elif "secret" in self.path:
                self.send_response(401)
                self.send_header("WWW-Authenthicate","Basic realm='OpenFDA Private Zone")
                self.end_headers()

            elif "redirect" in self.path:
                self.send_response(302)
                self.send_header('Location', 'http://localhost:8000/')
                self.end_headers()




        except KeyError:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open("error.html","r") as f:
                file = f.read()
            self.wfile.write(bytes(file, "utf8"))






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
