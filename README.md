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

Here are some queries against database x:

 - Contents of the database:
 
```
$ curl -s admin:admin@localhost:5984/x/_all_docs?include_docs=true |fgrep -v _design | jq '.'
{
  "total_rows": 5,
  "offset": 0,
  "rows": [
    {
      "id": "angelo",
      "key": "angelo",
      "value": {
        "rev": "1-336fe31318567739882e3c38d20cf4fe"
      },
      "doc": {
        "_id": "angelo",
        "_rev": "1-336fe31318567739882e3c38d20cf4fe",
        "votes": {
          "thing1": 50,
          "thing2": 51
        }
      }
    },
    {
      "id": "ed",
      "key": "ed",
      "value": {
        "rev": "1-5c29f84506770a5d5a06ee070cd7368f"
      },
      "doc": {
        "_id": "ed",
        "_rev": "1-5c29f84506770a5d5a06ee070cd7368f",
        "votes": {
          "thing1": 50
        }
      }
    },
    {
      "id": "fred",
      "key": "fred",
      "value": {
        "rev": "1-41104e62ead8e8c5956804453a009d1b"
      },
      "doc": {
        "_id": "fred",
        "_rev": "1-41104e62ead8e8c5956804453a009d1b",
        "votes": {
          "thing1": 90,
          "thing2": 20
        }
      }
    },
    {
      "id": "steve",
      "key": "steve",
      "value": {
        "rev": "1-775e8601ffc1c0d2b8abe348acd8b430"
      },
      "doc": {
        "_id": "steve",
        "_rev": "1-775e8601ffc1c0d2b8abe348acd8b430",
        "votes": {
          "thing1": 66,
          "thing2": 44
        }
      }
    }
  ]
}
```

 - Individual votes after proportional normalization (total == 100):
 
```
$ curl admin:admin@localhost:5984/x/_design/votes/_view/normal?reduce=false
{"total_rows":4,"offset":0,"rows":[
{"id":"angelo","key":"angelo","value":{"thing1":49,"thing2":50}},
{"id":"ed","key":"ed","value":{"thing1":100}},
{"id":"fred","key":"fred","value":{"thing1":81,"thing2":18}},
{"id":"steve","key":"steve","value":{"thing1":60,"thing2":40}}
]}
```

 - Voting statistics for each item:
 
```
$ curl admin:admin@localhost:5984/x/_design/votes/_view/votes?group=true
{"rows":[
{"key":"thing1","value":{"sum":290,"count":4,"min":49,"max":100,"sumsqr":22562}},
{"key":"thing2","value":{"sum":108,"count":3,"min":18,"max":50,"sumsqr":4424}}
]}
```

 - A less useful query: How many users voted (for anything)?
 
```
$ curl admin:admin@localhost:5984/x/_design/votes/_view/normal
{"rows":[
{"key":null,"value":4}
]}
```
