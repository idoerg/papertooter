# papertooter
A script to post manuscripts from BioRxiv to Mastodon using a unique hashtag based on the manuscript DOI.

## Purpose
The purpose of this program is to post ("toot") a BioRxiv preprint on the Mastodo social network. You would need a Mastodon account, and you would need to connect it to Mastodon using Mastodon.py. To post the bioarxiv preprint you would run the following from the command line:

`$ papertooter http://biorxiv.org/paper_url mastodon_credentials_file`

This will create a post on Mastodon using your account with the paper title, a hashtag based on the paper DOI, and a link to the paper. 

### Hashtag
The hashtag is based on the paper DOI. In Biorxiv the DOI is composed of alphanumberic characters, slashes and periods. Because hashtags do not allow persiods and slashes, a `/` is converted to a `__` (double underscore) and a `.` is converted to a `_` (single underscore). This allows for a unique tagging of the manuscript.

