import logging # pragma: no cover
import urllib.request # pragma: no cover
from bs4 import BeautifulSoup # pragma: no cover


def get_github_url(url):
    data = ''
    github_url = ''
    type = get_type(url)

    if type != -1:
        if type == 1: # npmjs url
            # web scrape npmjs page
            response = urllib.request.urlopen(url)
            data = response.read()
            #req = requests.get(url)
            soup = BeautifulSoup(data, features = 'html.parser')
            soup.prettify()
            links = []
            for anchor in soup.find_all('a', href = True): 
                if 'https://github.com' in anchor['href']: links.append(anchor['href'])
            github_url = links[0]
        else: github_url = url
    
    return github_url


def get_type(url):
    # urls must be either github or npmjs
    if 'github' not in url and 'npmjs' not in url: return -1

    url_type = 1 if 'npmjs' in url else 0          
    return url_type

