from request import Request
from user import user
from datetime import datetime
import subprocess
import os
from googlesearch import search
import youtube_dl
import multiprocessing
from multiprocessing import Pool

def download_all_requests(requests):
    threads_count = multiprocessing.cpu_count() # use all of the threads on the system that we can
    # Below are the hard coded values for the testing of the effectiveness of threads
    # threads_count = 1
    # threads_count = 2    
    # threads_count = 4
    # threads_count = 8
    with Pool(threads_count) as p:
        p.map(download_request, requests)
    subprocess.call(r'cd output; for i in */; do zip -r "${i%/}.zip" "$i"; done', shell=True)
    # The above code is the same as the code below, above will do it with as many threads as possible
    # for r in requests:
        # download_request(r)

def mkdir(path): #mkdir = Make Director, creates a folder if it does not exist
    if not os.path.exists(path):
        os.makedirs(path)
        
def download_request(r):
    if r.downloaded_status:
        return
    if r.kind == "URL": # we are dealing with a plain old HTTP request
        url = r.value
        path = "output/" + r.uuid
        download_from_url(url, path)
    if r.kind == "search":
        search_list = list(search(r.value, stop = 10)) # call the google_search library to get the list of urls for the search terms stored in r.value
        for i in range(len(search_list)): # it would nice to multithread this, but we are already multithreaded at the request level. More work could be done to improve this system.
            url = search_list[i]
            path = 'output/' + r.uuid + '/' + str(i + 1) + '/'
            if ('youtube' not in url): # Youtube vidoes are not going to be able to work, those will be for the youtube request
                download_from_url(url, path)
            else:
                download_from_youtube(url, path)
    if r.kind == "youtube":
        path = "output/" + r.uuid + '/'
        download_from_youtube(r.value, path)
    if r.kind == "ipfs":
        path = "output/" + r.uuid + '/'
        download_from_ipfs(r.value, path)
    r.set_file_location(path)
    r.set_downloaded_status(True)

    # mark_as_downloaded(p) # this is where this function will intergrate with data managment to update the file location and downlaoded status

def download_from_url(url, path):
    mkdir(path)
    subprocess.call(r'wget -E -H -k -K -p -P ' + path + ' ' +  url + ' robots=off ', shell=True)

def download_from_youtube(url, path):
    mkdir(path)
    ydl_opts = {
        'outtmpl': path + '%(title)s' # add title to file name
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_from_ipfs(ipfs_hash, path):
    mkdir(path)
    subprocess.call(r'ipfs get ' + ipfs_hash + ' -o ' + path, shell=True) #this requires the IPFS daemon running

# def main():
    #requests = get_all_requests() # This is where command and control will interafce with Data Managment. It will return the list of requests from the database.
    # requests = [] # Because we can't do the above method, we are going to create a mock list with requests
    # tests
    # requests.append(Request("URL", "https://www.gutenberg.org/cache/epub/2265/pg2265.txt", user("Jake", "Vossen", "jakevossen", "asdf"), datetime.now()))
    # requests.append(Request("URL", "https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/46507.pdf", user("Jake", "Vossen", "jakevossen", "asdf"), datetime.now()))
    # requests.append(Request("URL", "https://en.wikipedia.org/wiki/Monty_Python_and_the_Holy_Grail", user("Jake", "Vossen", "jakevossen", "asdf"), datetime.now()))
    # requests.append(Request("search", "What Is the Airspeed Velocity of an Unladen Swallow?", user("Jake", "Vossen", "jakevossen", "asdf"), datetime.now()))
    # requests.append(Request("search", "Library of Congress", user("Jake", "Vossen", "jakevossen", "asdf"), datetime.now()))    
    # requests.append(Request("youtube", "https://www.youtube.com/watch?v=NtrVwX1ncqk", user("Jake", "Vossen", "jakevossen", "asdf"), datetime.now()))
    # requests.append(Request("youtube", "https://www.youtube.com/watch?v=Gbtulv0mnlU", user("Jake", "Vossen", "jakevossen", "asdf"), datetime.now()))
    # requests.append(Request("ipfs", "/ipfs/QmS4ustL54uo8FzR9455qaxZwuMiUhyvMcX9Ba8nUH4uVv/readme", user("Jake", "Vossen", "jakevossen", "asdf"), datetime.now()))
    # requests.append(Request("ipfs", "/ipfs/QmVLTMHtLRhnft3QspDx4qTJeXY6hiib1j77UfQmY54CGe/mosaic.png", user("Jake", "Vossen", "jakevossen", "asdf"), datetime.now()))    
    
    # download_all_requests(requests)

# main() # start the program
