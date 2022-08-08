from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from flask import Flask, request, render_template,jsonify

hostName = "localhost"
serverPort = 8000

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        test = 'new test'
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>URL shortener</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        print("space")
        print("test")
        print(self.path)
        link = ''
        if self.path!='/favicon.ico':
            #print(type(self.path))
            link = self.path[10:]
            print(link)
            self.wfile.write(bytes(link,"utf-8"))
        self.wfile.write(bytes(' <form><label for="fname">URL link</label> <br>  <input type="text" id="urllink" name="urllink"><br></form>',"utf-8"))
        
        self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

