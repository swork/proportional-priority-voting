from quart_trio import QuartTrio
import httpx

app = QuartTrio(__name__)

@app.route('/result')
async def get_result():
    return app.config['backend'].get_result()

@app.route('/identities')
async def get_identities():
    return app.config['backend'].get_identities()

@app.route('/ranking/<string:identity>')
async def get_ranking(identity):
    raw = request.args.get('raw')
    return app.config['backend'].get_ranking(identity, raw=raw)

@app.route('/ranking/<string:identity>', methods=['PUT'])
async def put_ranking(identity, rankings, rev):
    return app.config['backend'].put_ranking(identity, rankings, rev)

if __name__ == '__main__':
    session = httpx.session()
    instancePrefix = 'http://10.9.4.246:5984/'
    instanceToken = 'get me some'
    dbName = 'x'
    app.config['backend'] = PriorityVotingCouchDB(session,
                                                  instancePrefix,
                                                  instanceToken,
                                                  dbName)
    app.run()
