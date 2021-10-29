# Since the main purpose for me to create this was to back up my
# history so I could extend my https://github.com/seanbreckenridge/HPI,
# this makes the pushshift exports a similar interface to the
# https://github.com/karlicoss/rexport/ DAL
# The underlying JSON may have different values, but as long
# as the properties I want are implemented, can do some
# runtime checks to resolve type conflicts/structure

import json
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, Iterator, NamedTuple, cast

Json = Dict[str, Any]

# https://www.reddit.com/dev/api
TYPE_PREFIX = re.compile("t[1-6]_")


def _remove_type_prefix(link: str) -> str:
    if re.match(TYPE_PREFIX, link):
        return link[3:]
    else:
        return link


def reddit(suffix: str) -> str:
    return "https://reddit.com" + suffix


# named PComment (pushshift comment) so that cachew
# doesn't get confused
class PComment(NamedTuple):
    raw: Json

    @property
    def id(self) -> str:
        return cast(str, self.raw["id"])

    @property
    def created(self) -> datetime:
        return datetime.fromtimestamp(self.raw["created_utc"], tz=timezone.utc)

    @property
    def url(self) -> str:
        if "permalink" not in self.raw:
            r = self.raw
            # old items don't have permalinks, reconstruct from link_id/parent_id
            # https://www.reddit.com/dev/api - search 'type prefix'
            link_id = _remove_type_prefix(r["link_id"])
            parent_id = _remove_type_prefix(r["parent_id"])
            return reddit(f"/r/{r['subreddit']}/comments/{link_id}/x/{parent_id}/")
        else:
            return reddit(self.raw["permalink"])

    @property
    def text(self) -> str:
        return cast(str, self.raw["body"])


# I only ever do one export of this, so don't need to worry
# about merging duplicates here. However, will have to merge
# in HPI
def read_file(p: Path) -> Iterator[PComment]:
    with p.open("r") as cf:
        items = json.load(cf)
    for comm in items:
        yield PComment(raw=comm)
