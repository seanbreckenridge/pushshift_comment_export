# pushshift_comment_export

Exports all accessible reddit comments for an account using pushshift.

Reddit (supposedly) only indexes the last 1000 items per query, so there are lots of comments that I don't have access to using the official reddit API (I run [`rexport`](https://github.com/karlicoss/rexport/) periodically to pick up any new data.)

This downloads all the comments that pushshift has, which is typically more than the 1000 query limit. This is only really meant to be used once per account, to access old data that I don't have access to.

For context see the comments [`here`](https://github.com/karlicoss/rexport/#api-limitations). From what I've read on random reddit threads, doesn't seem reddit's GDPR process is worked out yet either, so not sure if that sending their legal team a request would work out well.

```
$ ps_comments export <reddit_username> --to-file ./data.json
.....
[D 200903 19:51:49 __init__:43] Have 4700, now searching for comments before 2015-10-07 23:32:03...
[D 200903 19:51:49 __init__:17] Requesting https://api.pushshift.io/reddit/comment/search?author=username&limit=100&sort_type=created_utc&sort=desc&before=1444260723...
[D 200903 19:51:52 __init__:43] Have 4800, now searching for comments before 2015-09-22 13:55:00...
[D 200903 19:51:52 __init__:17] Requesting https://api.pushshift.io/reddit/comment/search?author=username&limit=100&sort_type=created_utc&sort=desc&before=1442930100...
[D 200903 19:51:57 __init__:43] Have 4860, now searching for comments before 2014-08-28 07:10:14...
[D 200903 19:51:57 __init__:17] Requesting https://api.pushshift.io/reddit/comment/search?author=username&limit=100&sort_type=created_utc&sort=desc&before=1409209814...
[I 200903 19:52:01 __init__:64] Done! writing 4860 comments to file ./data.json
```

pushshift doesn't require authentication, if you want to preview what this looks like, just go to <https://api.pushshift.io/reddit/comment/search?author={username}>

### Install

Requires `python3.6+`

To install with pip, run:

    pip install 'git+https://github.com/seanbreckenridge/pushshift_comment_export'

(Installs as `ps_comments`)
