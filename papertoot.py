#!/usr/bin/env python

import sys
from bs4 import BeautifulSoup as BS
import requests
from mastodon import Mastodon

def doi_to_hashtag(doi):
    '''
    converts a DOI to hashtag
    _ for a .
    __ for a  /
    '''
    hashtag = doi.replace('.','_')
    hashtag = hashtag.replace('/','__')
    hashtag = '#' + hashtag
    return hashtag

def parse_info(url):
    ''' parses the doi, title, url, given a biorxiv url'''
    req = requests.get(url)
    html_doc = req.text
    soup = BS(html_doc, 'html.parser')
    doi = soup.find("meta", {"name": "citation_doi"})["content"]
    # Commented out lines below are for arxiv.org Needs work
    title = soup.find("meta", {"name": "DC.Title"})["content"]
    # title = soup.find("meta", {"name": "citation_title"})["content"]
    public_url = soup.find("meta", {"name": "citation_public_url"})["content"]
    # public_url = soup.find("meta", {"name": "citation_pdf_url"})["content"]
    return (doi, title, public_url)

def toot_article(hashtag, title, public_url):
    toot = mastodon.toot(f'{title} {hashtag}\n {public_url}')

if __name__ == '__main__':
    doi, title, public_url = parse_info(sys.argv[1])    
    hashtag = doi_to_hashtag(doi)
    mastodon = Mastodon(access_token = sys.argv[2])
    toot_article(hashtag, title, public_url)
