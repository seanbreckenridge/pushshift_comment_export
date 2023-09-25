Exports all accessible reddit comments for an account using [pushshift](https://pushshift.io/).

[![PyPi version](https://img.shields.io/pypi/v/pushshift_comment_export.svg)](https://pypi.python.org/pypi/pushshift_comment_export) [![Python 3.6|3.7|3.8](https://img.shields.io/pypi/pyversions/pushshift_comment_export.svg)](https://pypi.python.org/pypi/pushshift_comment_export) [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

# REDDIT API CHANGES

Since the API restrictions on reddit, the terms of use for pushshift have changed, see <https://pushshift.io/signup>

I no longer use this (I only really used it once to get all my historical data), but in order to use this one would need to supply a pushshift API token. Since I don't meet the terms of use ('user certifies that they are a registered user of Reddit and a Reddit moderator (a “Mod") and may only access Reddit Services and Data through Pushshift Services for the express limited purposes of community moderation, enforcing Reddit community guidelines, and ensuring community member safety'), I don't see a reason to update this for myself, but if someone else wants to make a PR, feel free to do so.

You should be able to get your historical data through the [data request](https://www.reddit.com/settings/data-request), if all you want is to backup your data.

### Install

Requires `python3.6+`

To install with pip, run:

    pip install pushshift_comment_export

Is accessible as the script `pushshift_comment_export`, or by using `python3 -m pushshift_comment_export`.

---

Reddit (supposedly) only indexes the last 1000 items per query, so there are lots of comments that I don't have access to using the official reddit API (I run [`rexport`](https://github.com/karlicoss/rexport/) periodically to pick up any new data.)

This downloads all the comments that pushshift has, which is typically more than the 1000 query limit. This is only really meant to be used once per account, to access old data that I don't have access to.

For more context see the comments [here](https://github.com/karlicoss/rexport/#api-limitations).

Reddit has recently added a [data request](https://www.reddit.com/settings/data-request) which may let you get comments going further back, but pushshifts JSON response contains a bit more info than what the GDPR request does

Complies to the rate limit [described here](https://github.com/dmarx/psaw#features)

```
$ pushshift_comment_export <reddit_username> --to-file ./data.json
.....
[D 200903 19:51:49 __init__:43] Have 4700, now searching for comments before 2015-10-07 23:32:03...
[D 200903 19:51:49 __init__:17] Requesting https://api.pushshift.io/reddit/comment/search?author=username&limit=100&sort_type=created_utc&sort=desc&before=1444260723...
[D 200903 19:51:52 __init__:43] Have 4800, now searching for comments before 2015-09-22 13:55:00...
[D 200903 19:51:52 __init__:17] Requesting https://api.pushshift.io/reddit/comment/search?author=username&limit=100&sort_type=created_utc&sort=desc&before=1442930100...
[D 200903 19:51:57 __init__:43] Have 4860, now searching for comments before 2014-08-28 07:10:14...
[D 200903 19:51:57 __init__:17] Requesting https://api.pushshift.io/reddit/comment/search?author=username&limit=100&sort_type=created_utc&sort=desc&before=1409209814...
[I 200903 19:52:01 __init__:64] Done! writing 4860 comments to file ./data.json
```

pushshift doesn't require authentication, if you want to preview what this looks like, just go to <https://api.pushshift.io/reddit/comment/search?author=>

#### Usage in HPI

This has been merged into [karlicoss/HPI](https://github.com/karlicoss/HPI), which combines the periodic results of `rexport` (to pick up new comments), with any from the past using this, which looks like [this](https://github.com/karlicoss/HPI/tree/master/my/reddit); my config looking like:

```reddit
class reddit:
    class rexport:
        export_path: Paths = "~/data/rexport/*.json"
    class pushshift:
        export_path: Paths = "~/data/pushshift/*.json"
```

Then importing from `my.reddit.all` combines the data from both of them:

```
>>> from my.reddit.rexport import comments as rcomments
>>> from my.reddit.pushshift import comments as pcomments
>>> from my.reddit.all import comments
>>> from more_itertools import ilen
>>> ilen(rcomments())
1020
>>> ilen(pcomments())
4891
>>> ilen(comments())
4914
```
