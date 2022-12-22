import httpx
import trio
import click
import os.path
import logging
import json

logger = logging.getLogger(__name__)

async def install_design_docs(db: str) -> None:
    ddoc_dir = os.path.dirname(__file__)
    with open(os.path.join(ddoc_dir, "_design/votes.json"), 'r') as f:
        file_content = json.load(f)
    async with httpx.AsyncClient() as client:
        create_response = await client.put(db)
        try:
            create_response.raise_for_status()
        except:
            get_content = {}

        get_response = await client.get(db + '/_design/votes')
        try:
            get_response.raise_for_status()
        except:
            get_content = {}
        else:
            get_content = get_response.json()

        get_rev = get_content.get('_rev', None)
        if get_rev:
            del get_content['_rev']

        if file_content == get_content:
            logger.info('_design/votes is unchanged')
        else:
            params = {}
            if get_rev:
                params['rev'] = get_rev


            # db = 'http://localhost:5555/x'


            put_response = await client.put(db + '/_design/votes',
                                            params=params,
                                            json=file_content)
            put_response.raise_for_status()
            logger.info('_design/votes updated')

@click.command()
@click.argument("db", type=str)  #, help="URL of CouchDB database ('.../dbname')")
def main(db: str) -> int:
    try:
        trio.run(install_design_docs, db)
    except:
        logger.exception('Problem')
        return 1
    else:
        return 0

if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    main()
