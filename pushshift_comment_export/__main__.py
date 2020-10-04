import time
import json
from datetime import datetime
from typing import Optional, Dict, Any, List

import requests
import click
import backoff  # type: ignore[import]
from logzero import logger  # type: ignore[import]

BASE_PUSHSHIFT_URL = "https://api.pushshift.io/reddit/comment/search?author={}&limit=100&sort_type=created_utc&sort=desc"  # &before=epochint

# rate limiter for pushshift
@backoff.on_exception(backoff.expo, requests.exceptions.RequestException)
def ps_request(url: str) -> Dict[str, Any]:
    logger.debug("Requesting {}...".format(url))
    resp: requests.Response = requests.get(url)
    time.sleep(2)
    resp.raise_for_status()
    data: Dict[str, Any] = resp.json()["data"]
    return data


# paginate through pushshift comments for a user, by specifying an epoch time
# to receive comments before
# once we receive the first chunk of comments, use the epoch time of the
# last currently known comment, and filter anything that was posted after that
def create_url(reddit_username: str, before: Optional[int]) -> str:
    if before is None:
        return BASE_PUSHSHIFT_URL.format(reddit_username)
    else:
        return BASE_PUSHSHIFT_URL.format(reddit_username) + f"&before={before}"


def request_all_comments(reddit_username: str) -> List[Dict[str, Any]]:
    prev_created_utc: Optional[int] = None
    all_comments: List[Dict[str, Any]] = []
    while True:
        url: str = create_url(reddit_username, before=prev_created_utc)
        new_comments = ps_request(url)
        all_comments.extend(new_comments)
        if len(new_comments) == 0:  # exhausted all paginations
            break
        prev_created_utc = all_comments[-1]["created_utc"]
        assert prev_created_utc is not None
        logger.debug(
            f"Have {len(all_comments)}, now searching for comments before {datetime.utcfromtimestamp(prev_created_utc)}..."
        )
    return all_comments


@click.command()
@click.argument("REDDIT_USERNAME")
@click.option(
    "--to-file",
    type=click.Path(),
    required=True,
    help="File to store downloaded comments to",
)
def main(reddit_username: str, to_file: str) -> None:
    """
    Download all comments from a user to a JSON file
    """
    all_comments = request_all_comments(reddit_username)
    logger.info(f"Done! writing {len(all_comments)} comments to file {to_file}")
    with open(to_file, "w") as to_f:
        json.dump(all_comments, to_f)


if __name__ == "__main__":
    main()
