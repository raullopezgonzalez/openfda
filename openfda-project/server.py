import http.server
import socketserver
import json
import http.client

# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 8000
socketserver.TCPServer.allow_reuse_address = True

class OpenFDAHTML():
    def html_visual(self, list_1):

        intro = "<!doctype html>" + "\n" + "<html>" + "\n" + "<body>" + "\n" "<ul>" + "\n"
        end = "</ul>" + "\n" + "</body>" + "\n" + "</html>"

        with open("drug.html", "w") as f:
            f.write(intro)
            for element in list_1:
                element_1 = "<li>" + element + "</li>" + "\n"
                f.write(element_1)
            f.write(end)

HTML = OpenFDAHTML()

class OpenFDAClient():
    def communicate_active(self,drug,limit):
        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")
        url = "/drug/label.json?search=active_ingredient:" + drug + "&" + "limit=" + limit
        conn.request("GET", url, None, headers)
        r1 = conn.getresponse()
        drugs_raw = r1.read().decode("utf-8")
        conn.close()
        drug = json.loads(drugs_raw)
        drugs_1 = drug
        return drugs_1




    def communicate_company(self,drug,limit):
        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")
        url_1 = "/drug/label.json?search=manufacturer_name:" + drug + "&" + "limit=" + limit
        conn.request("GET", url_1, None, headers)
        r1 = conn.getresponse()
        drugs_raw = r1.read().decode("utf-8")
        conn.close()
        drug = json.loads(drugs_raw)
        drugs_1 = drug
        return drugs_1

    def communicate_list(self,limit):
        headers = {'User-Agent': 'http-client'}
        conn = http.client.HTTPSConnection("api.fda.gov")
        url = "/drug/label.json?" + "limit=" + limit
        conn.request("GET", url, None, headers)
        r1 = conn.getresponse()
        drugs_raw = r1.read().decode("utf-8")
        conn.close()
        drug = json.loads(drugs_raw)
        drugs_1 = drug
        return drugs_1

Client = OpenFDAClient()



class OpenFDAParser():
    def extract_data_sdrugs(self, drugs_1, list_1):
        for i in range(len(drugs_1['results'])):
            if 'active_ingredient' in drugs_1['results'][i]:
                list_1.append(drugs_1['results'][i]['active_ingredient'][0])
            else:
                list_1.append("Unknown")

    def extract_data_scompany(self,drugs_1,list_1):
        for i in range(len(drugs_1['results'])):
            try:
                if "openfda" in drugs_1['results'][i]:
                    list_1.append(drugs_1['results'][i]['openfda']["manufacturer_name"][0])
            except KeyError:
                list_1.append("Unknown")

    def extract_data_ldrugs(self,drugs_1,list_1):
        for i in range(len(drugs_1['results'])):
            try:
                if "openfda" in drugs_1["results"][i]:
                    list_1.append(drugs_1['results'][i]['openfda']["brand_name"][0])
            except KeyError:
                list_1.append("Unknown")

    def extract_data_lcompanies(self,drugs_1,list_1):
        for i in range(len(drugs_1['results'])):
            try:
                if "openfda" in drugs_1['results'][i]:
                    list_1.append(drugs_1['results'][i]['openfda']["manufacturer_name"][0])
            except KeyError:
                list_1.append("Unknown")

    def extract_data_warnings(self,drugs_1,list_1):
        for i in range(len(drugs_1['results'])):
            if "warnings" in drugs_1["results"][i]:
                list_1.append(drugs_1['results'][i]['warnings'][0])
            else:
                list_1.append("Unknown")

Parser = OpenFDAParser()






# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):

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

                list_1=[]

                if "&" not in self.path:
                    limit = "10"
                    params = self.path.split("?")[1]
                    drug = params.split("&")[0].split("=")[1]

                    alpha = Client.communicate_active(drug, limit)

                    Parser.extract_data_sdrugs(alpha, list_1)

                elif "&" in self.path:
                    params = self.path.split("?")[1]
                    drug = params.split("&")[0].split("=")[1]
                    limit = params.split("&")[1].split("=")[1]
                    if not limit:
                        limit = "10"

                    alpha = Client.communicate_active(drug, limit)

                    Parser.extract_data_sdrugs(alpha, list_1)

                HTML.html_visual(list_1)

                with open("drug.html", "r") as f:
                    file = f.read()

                self.wfile.write(bytes(file, "utf8"))

            elif "searchCompany" in self.path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                list_1=[]

                if "&" not in self.path:
                    limit = "10"
                    params = self.path.split("?")[1]
                    drug = params.split("&")[0].split("=")[1]

                    beta = Client.communicate_company(drug, limit)

                    Parser.extract_data_scompany(beta, list_1)

                elif "&" in self.path:
                    params = self.path.split("?")[1]
                    drug = params.split("&")[0].split("=")[1]
                    limit = params.split("&")[1].split("=")[1]

                    if not limit:
                        limit = "10"

                    omega = Client.communicate_company(drug, limit)

                    Parser.extract_data_scompany(omega, list_1)

                HTML.html_visual(list_1)

                with open("drug.html", "r") as f:
                    file = f.read()

                self.wfile.write(bytes(file, "utf8"))

            elif "listDrugs" in self.path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                list_1=[]
                params = self.path.split("?")[1]
                limit = params.split("=")[1]

                landa = Client.communicate_list(limit)

                Parser.extract_data_ldrugs(landa, list_1)

                HTML.html_visual(list_1)

                with open("drug.html", "r") as f:
                    file = f.read()

                self.wfile.write(bytes(file, "utf8"))

            elif "listCompanies" in self.path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                list_1 = []
                params = self.path.split("?")[1]
                limit = params.split("=")[1]

                phi = Client.communicate_list(limit)

                Parser.extract_data_lcompanies(phi, list_1)

                HTML.html_visual(list_1)

                with open("drug.html", "r") as f:
                    file = f.read()

                self.wfile.write(bytes(file, "utf8"))

            elif "listWarnings" in self.path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                list_1 = []
                params = self.path.split("?")[1]
                limit = params.split("=")[1]

                pi = Client.communicate_list(limit)

                Parser.extract_data_warnings(pi, list_1)

                HTML.html_visual(list_1)


                with open("drug.html", "r") as f:
                    file = f.read()

                self.wfile.write(bytes(file, "utf8"))

            elif "secret" in self.path:
                self.send_response(401)
                self.send_header("WWW-Authenticate","Basic realm='OpenFDA Private Zone")
                self.end_headers()

            elif "redirect" in self.path:
                self.send_response(302)
                self.send_header('Location', 'http://localhost:8000/')
                self.end_headers()

            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open("error.html", "r") as f:
                    file = f.read()
                self.wfile.write(bytes(file, "utf8"))




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
print("final")


