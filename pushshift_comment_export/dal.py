# Since the main purpose for me to create this was to back up my
# history so I could extend my https://github.com/seanbreckenridge/HPI,
# this makes the pushshift exports a similar interface to the
# https://github.com/karlicoss/rexport/ DAL
# The underlying JSON may have different values, but as long
# as the properties I want are implemented, can do some
# runtime checks to resolve type conflicts/structure

import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, Iterator, NamedTuple, Set, Tuple

Json = Dict[str, Any]


def reddit(suffix: str) -> str:
    return "https://reddit.com" + suffix


# named PComment (pushshift comment) so that cachew
# doesn't get confused
class PComment(NamedTuple):
    raw: Json

    @property
    def created(self) -> datetime:
        return datetime.fromtimestamp(self.raw["created_utc"], tz=timezone.utc)

    @property
    def url(self) -> str:
        if "permalink" not in self.raw:
            r = self.raw
            # old items don't have permanlinks, reconstruct from link_id/parent_id
            return reddit(
                f"/r/{r['subreddit']}/comments/{r['link_id']}/foo/{r['parent_id']}/"
            )
        else:
            return reddit(self.raw["permalink"])

    @property
    def text(self) -> str:
        body_text: str = self.raw["body"]
        return body_text


# I only ever do one export of this, so don't need to worry
# about merging duplicates here. However, will have to merge
# in HPI
def read_file(p: Path) -> Iterator[PComment]:
    # datetime utc, subreddit
    emitted: Set[Tuple[int, str]] = set()
    with p.open("r") as cf:
        items = json.load(cf)
    for comm in items:
        yield PComment(raw=comm)
