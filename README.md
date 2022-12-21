# proportional-priority-voting
Find consensus on a changing list of priorities stored in CouchDB.

Each item to be prioritized is a string, unique in the full set of items.

Every voter is identified by a string, also unique, and has 100 votes to be
assigned among the priorities.

Only the items they rank non-zero are affected by their vote; that is, leaving a
rank at zero says "I don't have an opinion about this item." Votes in their
package are normalized to 100 by proportionality: if the total of votes differs
from 100, all votes are scaled so the total comes as close to 100 as possible
with floored integers.

Scaling and vote tallying is done within Couchdb through map and reduce
functions.

A user's package of votes is implemented as an object:

{
    "_id": "userIdentity",
    "votes": {
        "importantToMe": 72,
        "sortOfImportant": 28
    }
}

