from flask import current_app, request
from elasticsearch8 import Elasticsearch


def main():
    #index_name = os.getenv('ELASTICSEARCH_INDEX')
    client = Elasticsearch (
        'https://elasticsearch-master.elastic.svc.cluster.local:9200',
        verify_certs = False,
        basic_auth=('elastic', 'elastic')
    )

    for obs in request.get_json(force=True):
        res = client.index(
            #index = index_name,
            index='accidents',
            id=obs["ACCIDENT_NO"],
            body=obs
        )
        current_app.logger.info(f'Indexed observation {obs["ACCIDENT_NO"]}')

    return 'ok'
