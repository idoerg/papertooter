# papertooter
A script to post any DOI-identified manuscripts to Mastodon with a unique hashtag based on the manuscript DOI.

## Purpose

The purpose of this program is to post ("toot") published papers or preprints
on the Mastodon social network. Each paper is posted with a unique hashtag that can be used to track it as the post is
boosted. The Fediverse does not allow for searching by URL or strings, but it does allow by hashtags.

You would need a Mastodon account, and you would need to connect it to Mastodon using Mastodon.py. To post
the paper you would run the following from the command line:

`$ python papertoot.py -c mastodon_user_credentials_file http://doi.org/paper_url `
 
or

`$ python papertoot.py -c mastodon_user_credentials_file paper_doi`


This will create a post on Mastodon using your account with the paper title, a hashtag based on the paper
DOI, and a link to the paper. 

### Prerequisites

+ Python3 (Tested with 3.11)
+ [crossref-commons](https://pypi.org/project/crossref-commons/)
+ [Mastodon.py](https://github.com/halcy/Mastodon.py)


### Register your app using Mastodon.py
Mastodon.py is a Python wrapper for the Mastodon API. You would need to create a _user credentials files_ to post from
papertooter to mastodon. Assuming you have a Mastodon account, you would need to first install Mastodon.py:

`pip3 install Mastodon.py`

Then register you app, login, and example Toot. Note that this doesn't work with 2FA.

```
 from mastodon import Mastodon

# Register your app! This only needs to be done once (per server, or when
# distributing rather than hosting an application, most likely per device and server).
# Uncomment the code and substitute in your information:
'''
Mastodon.create_app(
    'your_app_name_here',
    api_base_url = 'https://mastodon.social', # your Mastodon instance. 
    to_file = 'pytooter_clientcred.secret'
)
'''

# Then, log in. This can be done every time your application starts (e.g. when writing a
# simple bot), or you can use the persisted information:
mastodon = Mastodon(client_id = 'pytooter_clientcred.secret',)
mastodon.log_in(
    'my_login_email@example.com',
    'incrediblygoodpassword',
    to_file = 'pytooter_usercred.secret'
)

# Note that this won't work when using 2FA - you'll have to use OAuth, in that case.
# To post, create an actual API instance:
mastodon = Mastodon(access_token = 'pytooter_usercred.secret')
mastodon.toot('Tooting from Python using #mastodonpy !')
```

`pytooter_usercred.secret` is the Mastodon user credit file you should use.

### Hashtag

The hashtag is based on the paper DOI. papertooter uses shortdoi.org, which accepts a DOI and provides a short DOI in the
form of  10/abcde. papertooter then creates a hashtag that is #abcde

In the example below I will run in with -v (verbose) and -s (silent: do not actually toot). There are options are
recommended when learning to use pytooter.

Example:
```
python papertoot.py -vs 'https://doi.org/10.1038/s41594-022-00758-y'
```

Outputs:
```
doi 10.1038/s41594-022-00758-y

title CENP-N promotes the compaction of centromeric chromatin
public url https://doi.org/10.1038/s41594-022-00758-y
hashtag #grhhvt
```


This shows the title, hashtag & link with which the toot will be made. To toot just remove the `-s`.

```
# Warning: this will actually Toot!
python papertoot.py -c your_user_credit_file 'https://doi.org/10.1038/s41594-022-00758-y'
```

It is also possible (but not recommended) to create a long hashtag. Because hashtags do not allow periods and slashes, a `/` is converted to a `__`
(double underscore) and any other non-alphanumeric os underscore character is converted to a `_` (single underscore). This allows for a (mostly)
unique tagging of the manuscript. So the DOI `DOI:10.1101/2022.11.28.518265` will be converted to `#10_1101__2022_11_28_518265`.


 
 
### Command line options:

```
-h, --help               show this help message and exit
-v, --verbose            debug information mostly
-s, --silent             silent: do not toot
-l, --long               long hashtag (defualt: short)
-c CREDS, --creds CREDS  Mastodon user credentials file

```


### Example:

![Toot](mytoot.png)


