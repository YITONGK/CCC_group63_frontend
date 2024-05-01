import requests
import json
from elasticsearch8 import Elasticsearch


def main():
    # return "check connection"

    url = "https://discover.data.vic.gov.au/api/3/action/datastore_search"
    resource_id = "d48aa391-9f43-4c67-bd90-81192ff2e732"
    limit = 100
    offset = 155665
    end_point = 167110
    client = Elasticsearch(
        "https://elasticsearch-master.elastic.svc.cluster.local:9200",
        verify_certs=False,
        basic_auth=("elastic", "elastic"),
    )
    while offset <= 155766:
        params = {"resource_id": resource_id, "limit": limit, "offset": offset}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            records = data["result"]["records"]
            for obs in records:
                data = obs["_id"]
                obs.pop("_id", None)
                client.index(index="accidents", id=data, body=obs)
            # if len(records) < limit:
            #     break
            offset += limit
        else:
            print("Failed to fetch data, status code:", response.status_code)
            break
    return "successful Insertion!"


main()
