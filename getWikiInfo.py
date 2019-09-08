#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 16:00:06 2019

@author: keziah
"""

import re
import wptools

def getInfo(name):
    
    # if title doesn't exist, no error is thrown
    page = wptools.page(name)
    try:
        prs = page.get_parse(show=False)
    except LookupError:
        msg = "Could not find Wikipedia article for '{}'".format(name)
        raise RuntimeError(msg)
        
    info = prs.data['infobox']
    if info is None:
        msg = "No infobox for Wikipedia article on '{}'".format(name)
        raise RuntimeError(msg)
        
    else:
        try:
            title = _getTitle(info)
            artist = _getArtist(info)
            artist = _capitalise(artist)
            year = _getYear(info)
            cover_url = _getImage(prs)
            return title, artist, year, cover_url
        except RuntimeError as err:
            raise RuntimeError(err)
    
    
def _capitalise(s):
    words = s.split(' ')
    words = [word.capitalize() for word in words]
    return ' '.join(words)


def _getTitle(data):
    try:
        return data['name']
    except KeyError:
        msg = "Could not find 'name' in infobox"
        raise RuntimeError(msg)
        
def _getArtist(data):
    try:
        artist = data['artist']
        artist = _checkLink(artist)
        return artist
    except KeyError:
        msg = "Could not find 'artist' in infobox"
        raise RuntimeError(msg)
        
def _getYear(data):
    try:
        released = data['released']
        srch = re.search(r'\d\d\d\d', released)
        year = srch.group() # will raise AttributeError if srch is None
        year = int(year)
        return year
    except:
        msg = "Could not find year in infobox"
        raise RuntimeError(msg)
        
def _getImage(parse):
    try:
        url = parse.data['image'][0]['url']
        return url
    except:
        msg = 'Could not find image url'
        raise RuntimeError(msg)
        
def _checkLink(s):
    """ Check if string `s` in a link in the info box, i.e. is wrapped in [[]].
    """
    return _checkDblBrackets(s, bracket='square')

def _checkList(s):
    """ Check if string `s` in a list(?) in the info box, i.e. is wrapped in 
        {{}}.
    """
    return _checkDblBrackets(s, bracket='curly')
    
def _checkDblBrackets(s, bracket='round'):
    """ Check if string `s` contains one or more sets of double brackets.
        If so, return the text within the brackets. 
        Otherwise return the original string.
         
        Parameters
        ----------
        s : str
            String to check
        bracket : {'round', 'square', 'curly'}
            Type of bracket to look for, i.e. (), [] or {}. Default is round.
            
        Returns
        -------
        String
    """
    string = _rmvDblBrackets(s, bracket=bracket)
    if string:
        return string
    else:
        return s
        
    
def _rmvDblBrackets(s, bracket='round'):
    """ Return text enclosed in double brackets from string `s`.
        
        Parameters
        ----------
        s : str
            String to check
        bracket : {'round', 'square', 'curly'}
            Type of bracket to look for,i.e. (), [] or {}. Default is round.
            
        Returns
        -------
        String. Will be empty if no double brackets of requested type are 
        present in `s`.
    """
    # get requested brackets
    brackets = {'round':['(', ')'], 'square':['[', ']'], 'curly':['{', '}']}
    br = brackets[bracket]
    # escape the brackets
    br = [re.escape(item) for item in br]
    # make regex to get the contents of double brackets
    regex = re.compile('{0}{0}(.*?){1}{1}'.format(*br))
    # iterator of sets of double brackets
    i = regex.finditer(s)

    # store items that are inside double brackets
    items = []

    # get items from the iterator
    while True:
        try:
            # get next match object
            m = next(i)
            # get text from within double brackets
            item = m.group(1)
            # put text in list
            items.append(item)
        except StopIteration:
            break
        
    # make single string of output
    output = ', '.join(items)
    
    return output


if __name__ == '__main__':
    
#    title = 'Bitches Brew'
#    title = 'Revolver (Beatles album)'
    title = 'Autobahn (album)'
    imgIdx = 2
    
    info = getInfo(title, imgIdx=imgIdx)
