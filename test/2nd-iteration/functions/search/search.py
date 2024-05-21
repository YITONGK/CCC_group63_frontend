from flask import request, current_app
import requests, logging, json



def main():
    r = requests.get("http://127.0.0.1:9090/_doc/weather",
        verify_certs=False,
        basic_auth=("elastic", "elastic"),
    )
    return r.json(), r.status_code
