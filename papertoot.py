#!/usr/bin/env python

import sys
import re 
import argparse 
from urllib.request import urlopen
import crossref_commons.retrieval
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
DOI_URL_RE = re.compile('http[s]{0,1}://doi.org')
DOI_RE_P = re.compile('10\.[0-9]{4,}')
DOI_RE = re.compile('10.\d{4,9}/[-._;()/:A-z0-9]+') 




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


def toot_article(mastodon, hashtag, title, public_url):
    toot = mastodon.toot(f'{title} {hashtag}\n {public_url}')

def get_doi(instr):
    pos = re.search(DOI_RE, instr)
    if not pos:
        return None
    doi = instr[pos.start():pos.end()]
    return doi 

def cli_parser():
    parser = argparse.ArgumentParser(
                prog = "papertoot",
                description = "Toots papers given their URLs")
    parser.add_argument('ident', 
           help="identifier of paper you want to toot. Must contain a DOI, no trailing characters")
    parser.add_argument('-v', '--verbose', action='store_true', help="debug information mostly") 
    parser.add_argument('-s', '--silent', action='store_true', help="silent: do not toot") 
    parser.add_argument('-l', '--longdoi', action='store_true', help="long doi form for the hashtag (default: short doi)") 
    parser.add_argument('-c', '--creds',  help="Mastodon user credentials file")
    return parser

def main():
    doi = ''
    title = ''
    public_url = ''
    parser = cli_parser()
    args = parser.parse_args()

    to_shorten = not args.longdoi
    ident = args.ident
    doi = get_doi(ident) 
    if not doi:
        raise ValueError("Does your identifier contain a DOI?")
    url = f'https://doi.org/{doi}'
    try:
        pub_metadata = crossref_commons.retrieval.get_publication_as_json(url)
    except ValueError:
        raise ValueError(f"Can't find publication. Did you provide an identifier that contains a DOI? Is the URL active?\n{url}")

    title = pub_metadata["title"][0]
    hashtag = doi_to_hashtag(doi, to_shorten)
    public_url = url
    if args.verbose:
        print(f"doi {doi}")
        print(f"title {title}")
        print(f"public url {public_url}")
        print(f"hashtag {hashtag}")
    if not args.silent:
        if args.creds:
            mastodon = Mastodon(access_token = args.creds)
            toot_article(mastodon, hashtag, title, public_url)
        else: 
            raise ValueError("You need creds to toot!")
         
if __name__ == '__main__':
    main()
