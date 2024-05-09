import requests
import json
from elasticsearch import Elasticsearch, helpers

def main():
    url = "http://router.fission.svc.cluster.local/extractdata"
    client = Elasticsearch(
        "https://elasticsearch-master.elastic.svc.cluster.local:9200",
        verify_certs=False,
        basic_auth=("elastic", "elastic"),
    )
    count = 0
    actions = []

    try:
        response = requests.get(url, verify=False)
        print(f"Request URL: {url}")
        print(f"Response Status Code: {response.status_code}")
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {"status": "error", "message": str(e)}

    data = response.json()
    for obs in data:
        action = {
            "_index": "accidents",
            "_id": obs["_id"],
            "_op_type": "index",
            "_source": {
                key: obs[key]
                for key in obs
                if key not in [
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
        if len(actions) == 500:
            helpers.bulk(client, actions)
            actions = []

    if actions:
        helpers.bulk(client, actions)

    return json.dumps({"status": 200, "message": "Successfully inserted records: " + str(count)})

# 调用 main 函数
if __name__ == "__main__":
    result = main()
    print(result)
