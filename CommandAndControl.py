from request import Request
from user import user
from datetime import datetime
import urllib.request
import urllib.parse
import re
import os
def download_all_requests(requests):
    for r in requests:
        download_request(r)

def download_request(r):
    if r.kind == "URL": # we are dealing with a plain old HTTP request
        url = r.value
        f = urllib.request.urlopen(url)
        html_contents = f.read().decode('ISO-8859-1')
        regex = re.compile('<title>(.*?)</title>', re.IGNORECASE|re.DOTALL)
        title = regex.search(html_contents).group(1)
        print("title:", title)
        
        newpath = "output/" + r.uuid 
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        file = open("output/" + r.uuid + "/" + title + ".html","w")
        file.write(html_contents)

    # file = open("/tmp/test.html","w")
    # file.write(str(f.read()))
    
def main():
    requests = []
    # tests
    requests.append(Request("URL", "https://www.google.com/", user("Jake", "Vossen", "jakevossen", "asdf"), datetime.now()))
    requests.append(Request("URL", "https://en.wikipedia.org/wiki/Monty_Python_and_the_Holy_Grail", user("Jake", "Vossen", "jakevossen", "asdf"), datetime.now()))
    
    download_all_requests(requests)

main()
