#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Make (or clear) the database.

Read the csv file, look up each album and add entry to database. The database
can then be filled with random test data, if desired.

If multiple options are provided, they will be executed in the following order:
    1) Clear the database
    2) Make the database
    3) Generate test data
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'albumratingsite.settings')

import django
django.setup()

import argparse
import random

from getWikiInfo import getInfo
from TakeItOrSleeveIt.models import Album

def makeDatabase():
    """ Get info from the Wikipedia pages of the albums listed in 
        data/albums.csv, and create entries in the database.
    """
    
    print('Getting data...')
    
    with open('data/albums.csv') as fileobj:
        text = fileobj.read()
        
    # split into list of lists
    albums = [album.split('\t') for album in text.split('\n') if album]
    header, *albums = albums
    
    failed = []
    
    for album in albums:
        # csv data
        title, artist, wiki = album
        # get info, either from Wiki article title or from album title
        try:
            if wiki:
                info = getInfo(wiki)
            else:
                info = getInfo(title)
        
            # unpack info
            title, artist, year, img = info
            # add to Album table in database
            a = Album(title=title, artist=artist, year=year, img=img)
            a.save()
            
        except Exception as err:
            failed.append(title)
            print(err)
        
    if len(failed) > 0:
        for fail in failed:
            print("Could not get info for '{}'".format(fail))
            
    else:
        print("Made database successfully!")
            
        
def clearDatabase():
    """ Remove all entries from the Albums table """
    Album.objects.all().delete()
    print("Cleared database")
    
    
def generateTestData():
    """ For every album in Albums, generate a random rating """
    all_albums = Album.objects.all()
    # for each album, generate a random number of votes
    for album in all_albums:
        n = 1000
        votes = random.randint(0, n)
        album.votes = votes
        album.contests = n
        album.rating = 100 * (album.votes / album.contests) # % rating
        album.save()
    print('Generated test data')
    
        
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=__doc__)
    
    parser.add_argument('-m', '--make', help='Make datadase', 
                        action='store_true')
    parser.add_argument('-c', '--clear', help='Clear database',
                        action='store_true')
    parser.add_argument('-t', '--test', help='Generate test data',
                        action='store_true')

    args = parser.parse_args()
    
    if args.clear:
        clearDatabase()
        
    if args.make:
        makeDatabase()
        
    if args.test:
        generateTestData()
    
    