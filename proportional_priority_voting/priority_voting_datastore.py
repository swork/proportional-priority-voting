from aiohttp import ClientSession
from copy import copy

class PriorityVotingDatastore:
    """Interact with persistent storage (CouchDB) for priorities voting.
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

    def getRankings(self, identity: str) -> (dict, dict):
        """Get existing priorities voting submission, normalized and raw.
        If raw exists, you'll need its _rev to update it.
        """
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

        # Get their accepted rankings after normalization
        path = self._couchInstancePrefix
        path += f'/{self._couchVotesDbName}/_design/normal/_view/normal'
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

        return (accepted.get('rows', {}).get('value', {}), submitted)

    def setMyRanking(self,
                     identity: str,
                     rankings: Union[(str, int), [str, int], dict],
                     rev: str) -> str:
        """Establish or replace a priorities voting submission.

        rev is _rev from previous raw submission, returned here or out of
        second item in .getRankings() return tuple.
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

