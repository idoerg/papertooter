#!/usr/bin/env python

import sys
import re 
import argparse 
from bs4 import BeautifulSoup as BS 
import requests 
from urllib.request import urlopen
from urllib.error import HTTPError
import json
from mastodon import Mastodon

##############################################################################
#
# Copyright 2022 Iddo Friedberg
# 
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program. If
# not, see <https://www.gnu.org/licenses/>. 
#
##############################################################################

SHORT_DOI_URL = "https://shortdoi.org/"
def shorten_doi(doi):
    doi_url = f"{SHORT_DOI_URL}{doi}?format=json"
    response = urlopen(doi_url)
    short_doi_data = json.loads(response.read())
    short_doi = short_doi_data['ShortDOI']
    return short_doi
    
def doi_to_hashtag(doi, to_shorten=True):
    '''
    converts a DOI to hashtag
    _ for all non alphanumeric or underscore characters.
    __ for a  /
    '''
    if to_shorten:
        doi = shorten_doi(doi)
        hashtag = re.sub("10\/","#",doi)
    else:   # long DOI
        # replace "/" with "__" (two underscores)
        hashtag = re.sub('\/','__', doi)
        #replace all other non-alphanumeric an non-underscore characters with "_"
        hashtag = re.sub('[^0-9a-zA-Z_]+','_', hashtag)
        hashtag = '#' + hashtag
    return hashtag

def parse_biorxiv_info(soup):
    ''' parses the doi, title, url, given a biorxiv or medrxiv url'''
    doi = soup.find("meta", {"name": "citation_doi"})["content"]
    title = soup.find("meta", {"name": "DC.Title"})["content"]
    public_url = soup.find("meta", {"name": "citation_public_url"})["content"]
    return (doi, title, public_url)

def parse_arxiv_info(soup):
    ''' parses the doi, title, url, given an arxiv url'''
    doi = soup.find("meta", {"name": "citation_doi"})["content"]
    title = soup.find("meta", {"name": "citation_title"})["content"]
    public_url = soup.find("meta", {"property": "og:url"})["content"]
    return (doi, title, public_url)

def toot_article(hashtag, title, public_url):
    toot = mastodon.toot(f'{title} {hashtag}\n {public_url}')

def archive_id(url):
    '''
    Identify the paper archive. 
    '''
    req = requests.get(url)
    html_doc = req.text
    site = None
    soup = BS(html_doc, 'html.parser')
    tag = soup.find("meta", {"property": "og:site_name"})
    if tag:
        if tag["content"].lower() == "arxiv.org":
            site = "arxiv"
        elif tag["content"].lower() == "biorxiv":
            site = "biorxiv"
        elif tag["content"].lower() == "medrxiv":
            site = "medrxiv"
    return site, soup
 

def cli_parser():
    parser = argparse.ArgumentParser(
                prog = "papertoot",
                description = "Toots papers given their URLs")
    parser.add_argument('url', help="url of paper you want to toot")
    parser.add_argument('-v', '--verbose', action='store_true', help="debug information mostly") 
    parser.add_argument('-s', '--silent', action='store_true', help="silent: do not toot") 
    parser.add_argument('-l', '--longdoi', action='store_true', help="long doi form for the hashtag (default: short doi)") 
    parser.add_argument('-c', '--creds',  help="Mastodon user credentials file")
    return parser
         
if __name__ == '__main__':
    doi = ''
    title = ''
    public_url = ''
    parser = cli_parser()
    args = parser.parse_args()
#   This was stuff 
#    site, soup = archive_id(args.url)
#    to_shorten = not args.longdoi
#    if site == "biorxiv" or site == "medrxiv":
#        doi, title, public_url = parse_biorxiv_info(soup)
#        hashtag = doi_to_hashtag(doi, to_shorten)
#    elif site == "arxiv":
#        doi, title, public_url = parse_arxiv_info(soup)
#        hashtag = doi_to_hashtag(doi, to_shorten)
#    else:
#        raise ValueError(f"url {url} not identified to be in a covered site (biorxiv, medrxiv, arxiv)")
    to_shorten = not args.longdoi
    pub_metadata = crossref_commons.retrieval.get_publication_as_json(url)
    title = pub_metadata["title"]
    hashtag = doi_to_hashtag(doi, to_shorten)
    
    if args.verbose:
        print(f"doi {doi}")
        print(f"title {title}")
        print(f"public url {public_url}")
        print(f"hashtag {hashtag}")
    if not args.silent:
        if args.creds:
            mastodon = Mastodon(access_token = args.creds)
            toot_article(hashtag, title, public_url)
        else: 
            raise ValueError("You need creds to toot!")
