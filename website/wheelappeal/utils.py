import requests
import json

def post_truck_data(data, endpoint="http://wheelappeal.co:5000/v1/submit"):
    url = "http://wheelappeal.co:5000/submit"
    headers = {
        'Content-Type': "application/json"
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response
