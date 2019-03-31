from request import Request
from user import user
from datetime import datetime
import subprocess
import os

def download_all_requests(requests):
    for r in requests:
        download_request(r)

def download_request(r):
    if r.kind == "URL": # we are dealing with a plain old HTTP request
        url = r.value
        newpath = "output/" + r.uuid 
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        
        subprocess.call(r'wget -E -H -k -K -p ' '-P ' + newpath +' ' +  url + ' robots=off', shell=True)
        

    # file = open("/tmp/test.html","w")
    # file.write(str(f.read()))


def main():
    requests = []
    # tests
    requests.append(Request("URL", "https://www.google.com/", user("Jake", "Vossen", "jakevossen", "asdf"), datetime.now()))
    requests.append(Request("URL", "https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/46507.pdf", user("Jake", "Vossen", "jakevossen", "asdf"), datetime.now()))
    requests.append(Request("URL", "https://en.wikipedia.org/wiki/Monty_Python_and_the_Holy_Grail", user("Jake", "Vossen", "jakevossen", "asdf"), datetime.now()))

    
    download_all_requests(requests)

main()
