#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Make (or clear) the database.

Read the csv file, look up each album and add entry to database.
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'albumratingsite.settings')

import django
django.setup()

import argparse

from getWikiInfo import getInfo
from TakeItOrSleeveIt.models import Album

def makeDatabase():
    
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
    Album.objects.all().delete()
        
        
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=__doc__)
    
    parser.add_argument('-m', '--make', help='Make datadase', 
                        action='store_true')
    parser.add_argument('-c', '--clear', help='Clear database',
                        action='store_true')

    args = parser.parse_args()
    
    if args.clear:
        clearDatabase()
        
    if args.make:
        makeDatabase()
    
    