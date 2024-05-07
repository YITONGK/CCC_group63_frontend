import requests
import json
from elasticsearch8 import Elasticsearch, helpers

def main():
    url = "https://discover.data.vic.gov.au/api/3/action/datastore_search"
    resource_id = "d48aa391-9f43-4c67-bd90-81192ff2e732"
    limit = 5000
    offset = 140649
    end_point = 167300
    client = Elasticsearch(
        "https://elasticsearch-master.elastic.svc.cluster.local:9200",
        verify_certs=False,
        basic_auth=("elastic", "elastic"),
    )
    count = 0
    actions = []
    while offset <= end_point:
        params = {"resource_id": resource_id, "limit": limit, "offset": offset}

        try:
            response = requests.get(url, params=params, verify=False)
            if response.status_code == 200:
                data = response.json()
                records = data["result"]["records"]

                for obs in records:
                    action = {
                        "_index": "accidents",
                        "_id": obs["_id"],
                        "_op_type": "index",
                        "_source": {
                            key: obs[key]
                            for key in obs
                            if key
                            not in [
                                "_id",
                                "RMA",
                                "DAY_WEEK_DESC",
                                "DCA_CODE",
                                "DCA_DESC",
                                "LIGHT_CONDITION",
                                "POLICE_ATTEND",
                            ]
                        },
                    }
                    actions.append(action)
                    count += 1
                    if (
                        len(actions) == 500
                    ):
                        helpers.bulk(client, actions)
                        actions = []

                if len(records) < limit:
                    break
                offset += limit
            else:
                print("Failed to fetch data: " + str(response))
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    if actions:
        helpers.bulk(client, actions)
    return json.dumps(
        {"status": 200, "message": "Successfully inserted records: " + str(count)}
    )

