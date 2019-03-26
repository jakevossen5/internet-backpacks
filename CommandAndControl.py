from request import Request
from user import user
from datetime import datetime
import urllib.request
import urllib.parse

def download_all_requests(requests):
    for r in requests:
        download_request(r)

def download_request(r):
    if r.kind == "URL": # we are dealing with a plain old HTTP file
        url = r.value
        f = urllib.request.urlopen(url)
        print(f.read().decode('ISO-8859-1'))
    
def main():
    requests = []
    requests.append(Request("URL", "https://www.google.com/", user("Jake", "Vossen", "jakevossen", "asdf"), datetime.now()))
    requests.append(Request("URL", "https://en.wikipedia.org/wiki/Monty_Python_and_the_Holy_Grail", user("Jake", "Vossen", "jakevossen", "asdf"), datetime.now()))

    download_all_requests(requests)

main()
