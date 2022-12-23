from aiohttp import ClientSession
from copy import copy

class PriorityVotingCouchDB:
    """Implement proportional priority voting over CouchDB
    """

    def __init__(self,
                 session: aiohttp.ClientSession,
                 couchInstancePrefix: str,
                 couchInstanceAuthToken: str,
                 couchVotesDbName: str):
        self._session = session
        self._couchInstancePrefix = couchInstancePrefix
        self._couchVotesDbName = couchVotesDbName
        self._headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Cookie': couchInstanceAuthToken,
        }

    def get_result(self) -> [ dict ]:
        """Get aggregated priority voting results"""
        path = self._couchInstancePrefix
        path += f'/{self._couchVotesDbName}/_design/votes/_view/votes'
        query = {
            'group': True
        }
        async with self._session.get(path,
                                     headers=self._headers,
                                     query=query) as resp:
            resp.raise_for_status()
            result = await resp.json()
        return result.get('rows', {}).get('value', {})

    def get_rankings(self, identified: bool=False) -> [ Union[(dict, dict), (str, dict, dict)]]:
        raise RuntimeError("not implemented")

    def get_identities(self) -> [ str ]:
        """List all voters (whether or not they allocated any votes)"""
        path = self._couchInstancePrevix
        path += f'/{self._couchVotesDbName}/_all_docs'
        async with self._session.get(path,
                                     headers=self._headers) as resp:
            try:
                resp.raise_for_status()
            except HttpError as e:
                raise RuntimeError("Database trouble") from e
            result = await resp.json()
        return list(
            map(lambda x: x['_id'],
                filter(lambda x: x[0] != '_',
                       result.get('rows', []))))

    def get_ranking(self, identity: str, raw: bool=False) -> dict:
        """Get existing priorities voting submission, normalized or raw.
        If raw exists, you'll need its _rev in updates.
        """
        if raw:
            # Get what they've submitted already
            path = self._couchInstancePrefix
            path += f'/{self._couchVotesDbName}/{identity}'
            async with self._session.get(path,
                                         headers=self._headers) as resp:
                try:
                    resp.raise_for_status()
                except HttpError:
                    submitted = {}
                else:
                    submitted = await resp.json()
            result = submitted

        else:
            # Get their accepted rankings after normalization
            path = self._couchInstancePrefix
            path += f'/{self._couchVotesDbName}/_design/votes/_view/normal'
            query = {
                'key': identity,
                'include_docs': True
            }
            async with self._session.get(path,
                                         query=query,
                                         headers=self._headers) as resp:
                try:
                    resp.raise_for_status()
                except HttpError:
                    accepted = {}
                else:
                    accepted = await resp.json()
            result = accepted.get('rows', {}).get('value', {})

        return result


    def put_ranking(self,
                    identity: str,
                    rankings: Union[ [(str, int)], [[str, int]], dict ],
                    rev: str) -> str:
        """Establish or replace a priorities voting submission.

        rev is _rev from previous raw get_ranking, returned here or out of
        .get_ranking(identity, raw=True) return tuple.
        """
        path = self._couchInstancePrefix
        path += f'/{self._couchVotesDbName}/{identity}'
        query = {
            'rev': rev
        }
        data = {}
        data |= rankings
        async with self._session.put(path,
                                     query=query,
                                     headers=self._headers,
                                     data=data) as resp:
            result = await resp.json()
        return result.get('rev', None)

