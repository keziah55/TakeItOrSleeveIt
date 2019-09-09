#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get album data from the infobox on a Wikipedia page
"""

import bs4
import requests
import urllib.parse
import re

def getInfo(name):
    """ Returns the album title, artist, year and cover art url from a given
        Wikipedia page `name`.
    """
    
    title = re.sub(' ', '_', name)
    title = urllib.parse.quote_plus(title, safe='()')
    url = "https://en.wikipedia.org/wiki/{}".format(title)
    
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    
    # look for <table class="infobox vevent haudio">
    table = soup.find('table', attrs={'class':"infobox vevent haudio"})
    
    # get album title
    try:
        th = table.find('th', attrs={'class':"summary album"})
        title = th.text
    except AttributeError:
        msg = 'Could not find album title in infobox'
        raise RuntimeError(msg)
    
    # get img url
    a = table.find('a', attrs={'class':'image'})
    img = a.find('img')
    if 'srcset' in img.attrs.keys():
        img = img['srcset']
    elif 'src' in img.attrs.keys():
        img = img['src']
    else:
        msg = 'Could not find image url'
        raise RuntimeError(msg)
    try:
        img = img.split(' ')[0]
        if re.match(r'http', img) is None:
            img = 'https:' + img
    except:
        msg = 'Could not make image url'
        raise RuntimeError(msg)
    
    # get artist
    try:
        div = table.find('div', attrs={'class':"contributor"})
        artist = div.text
    except AttributeError:
        msg = "Could not find artist in infobox"
        raise RuntimeError(msg)
    
    # get year
    try:
        td = table.find('td', attrs={'class':"published"})
        released = td.text # will raise AttributeError if td is None
        srch = re.search(r'\d\d\d\d', released)
        year = srch.group() # will raise AttributeError if srch is None
        year = int(year)
    except AttributeError:
        msg = "Could not find year in infobox"
        raise RuntimeError(msg)
    
    return title, artist, year, img

if __name__ == '__main__':
    
#    title = 'Revolver (Beatles album)'
    title = "Sign o' the Times"
    
    title = re.sub(' ', '_', title)
    title = urllib.parse.quote_plus(title, safe='()')
    url = "https://en.wikipedia.org/wiki/{}".format(title)
    
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    
    # look for <table class="infobox vevent haudio">
    table = soup.find('table', attrs={'class':"infobox vevent haudio"})
    
    with open('prince.html', 'w') as fileobj:
        fileobj.write(table.prettify())
        