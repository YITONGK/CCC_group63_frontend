from flask import request, current_app
import requests, logging, json

def config(k):
    with open(f'/configs/default/shared-data/{k}', 'r') as f:
       return f.read()

def main():
    r = requests.get("http://127.0.0.1:9090",
            verify=False,
            auth=("elastic", "elastic"))
    return r.json(), r.status_code
