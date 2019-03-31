from request import Request
from user import user
from datetime import datetime
import subprocess
import os
from googlesearch import search
import youtube_dl

def download_all_requests(requests):
    for r in requests:
        download_request(r)

def download_request(r):

    if r.kind == "URL": # we are dealing with a plain old HTTP request
        url = r.value
        path = "output/" + r.uuid
        download_from_url(url, path)
    if r.kind == "search":
        search_list = list(search(r.value, stop = 10))
        for i in range(len(search_list)):
            url = search_list[i]
            path = 'output/' + r.uuid + '/' + str(i + 1) + '/'
            if ('youtube' not in url): # Youtube vidoes are not going to be able to work, those will be for the youtube request
                download_from_url(url, path)
            else: #leaving this out for now
                download_from_youtube(url, path)
    if r.kind == "youtube":
        path = "output/" + r.uuid + '/'
        download_from_youtube(r.value, path)

    # file = open("/tmp/test.html","w")
    # file.write(str(f.read()))
def download_from_url(url, path):
    if not os.path.exists(path):
        os.makedirs(path)
        
    subprocess.call(r'wget -E -H -k -K -p ' '-P ' + path + ' ' +  url + ' robots=off', shell=True)
def download_from_youtube(url, path):
    if not os.path.exists(path):
        os.makedirs(path)
    ydl_opts = {
        'outtmpl': path + '%(title)s'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
def main():
    requests = []
    # tests
    requests.append(Request("URL", "https://www.google.com/", user("Jake", "Vossen", "jakevossen", "asdf"), datetime.now()))
    requests.append(Request("URL", "https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/46507.pdf", user("Jake", "Vossen", "jakevossen", "asdf"), datetime.now()))
    requests.append(Request("URL", "https://en.wikipedia.org/wiki/Monty_Python_and_the_Holy_Grail", user("Jake", "Vossen", "jakevossen", "asdf"), datetime.now()))
    requests.append(Request("search", "What Is the Airspeed Velocity of an Unladen Swallow?", user("Jake", "Vossen", "jakevossen", "asdf"), datetime.now()))
    requests.append(Request("youtube", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", user("Jake", "Vossen", "jakevossen", "asdf"), datetime.now()))

    
    download_all_requests(requests)

main()
