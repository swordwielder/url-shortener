from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
from sqlite3 import Error
import random
import string


hostName = "localhost"
serverPort = 8000


dictionary = {}
shorturllist = []
class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        #initialize the http
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>URL shortener</title></head>", "utf-8"))
        self.wfile.write(bytes("<b>Only links with https:// will be replaced with a url shortener.  <br> All others will return an invalid link. <br>  In the text field, a https:// link can be entered or a short url link can be entered</b>", "utf-8"))
        
        print(self.path)
        link = ''
        self.wfile.write(bytes(' <form><label for="fname">URL link</label> <br>  <input type="text" id="urllink" name="urllink"><br></form>',"utf-8"))
        
        
        if self.path!='/favicon.ico' and self.path!='/':
            
            # print('self.path')
            # print(self.path)
            tobereplace = self.path[10:]
            
            # check if the link is valid all other will be rejected
            if 'https%3A%2F%2F' in tobereplace[:14]:
                # replace the : and // with the actual value
                link = tobereplace.replace('%2F', '/')
                link = link.replace('%3A',':')

                #for key
                print()
                #
                print(check_value_exist(dictionary, link))
                print(dictionary)
                if link in dictionary:
                    # if a link is already in the dictionary, give the current link that existed in dictionary
                    self.wfile.write(bytes('The short url is: %s' % dictionary[link],"utf-8"))
                    self.wfile.write(bytes('<br> ' , "utf-8"))
                    self.wfile.write(bytes('The original url is %s' % link,"utf-8"))
                    self.wfile.write(bytes('<br> ' , "utf-8"))
                    self.wfile.write(bytes('<a href={original}>{short}</a>'.format(short=dictionary[link] ,original= link),"utf-8" ))
                    self.wfile.write(bytes("</body></html>", "utf-8"))
                else:
                    #if a fresh link is entered, create the short link
                    shortened = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
                    shorturl = 'short.ly/'+shortened
                    # print(link)
                    # print(shorturl)


                    # add links to dictionary
                    dictionary[link] = shorturl
                    
                    # write the link information to the page
                    
                    #self.wfile.write(bytes(link,"utf-8"))
                    self.wfile.write(bytes('The short url is: %s' % shorturl,"utf-8"))
                    self.wfile.write(bytes('<br> ' , "utf-8"))
                    self.wfile.write(bytes('The original url is: %s' % link,"utf-8"))
                    self.wfile.write(bytes('<br> ' , "utf-8"))
                    self.wfile.write(bytes('<a href={original}>{short}</a>'.format(short=shorturl ,original= link),"utf-8" ))
                    self.wfile.write(bytes("</body></html>", "utf-8"))
                print(dictionary)
            else:
                # check all conditions if https:// is not entered
                link = tobereplace.replace('%2F', '/')
                link = link.replace('%3A',':')
                # if https is not entered, check if the link entered is a short.ly link 
                if check_value_exist(dictionary, link):
                    #print('elif is hit')
                    self.wfile.write(bytes('The short url is: %s' % link,"utf-8"))
                    self.wfile.write(bytes('<br> ' , "utf-8"))
                    self.wfile.write(bytes('The original url is: %s' % get_key(link),"utf-8"))
                    self.wfile.write(bytes('<br> ' , "utf-8"))
                    self.wfile.write(bytes('<a  href={original}>{short}</a>'.format(short=link ,original= get_key(link)),"utf-8"))
                    self.wfile.write(bytes("</body></html>", "utf-8"))
                else:  #if not a shortly link, reject the link and print error
                    self.wfile.write(bytes('<p>  INVALID link</p>' , "utf-8"))
                
                self.wfile.write(bytes("</body></html>", "utf-8"))
            #print(dictionary)


def get_key(val):
    for key, value in dictionary.items():
        if val == value:
            return key

#check if  value exists in dictionary
def check_value_exist(test_dict, value):
    do_exist = False
    for key, val in test_dict.items():
        if val == value:
            do_exist = True
    return do_exist

# to be expanded for database if more feature is to be added.

# def connect_db():
#     try:
#         conn = sqlite3.connect('url.db')  # You can create a new database by changing the name within the quotes
#         c = conn.cursor() # The database will be saved in the location where your 'py' file is saved

#         #create table query and execute
#         c.execute('''CREATE TABLE  IF NOT EXISTS  URL
#                 (Name TEXT PRIMARY KEY, Symbol TEXT)''')

#     except Error as e:
#         print(e)


# main function
if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

