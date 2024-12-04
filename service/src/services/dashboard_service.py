import requests

HOST = 'http://admin:admin@grafana:3000'
PUBLIC_DASHBOARD_UID = 'buoy-p'

def get_embed_url():
    endpoint = HOST + '/api/dashboards/uid/buoy/public-dashboards/'

    find_response = requests.get(url=endpoint)
    if find_response.status_code == 200:
        # public dashboard already exists
        find_response_json = find_response.json()
        find_access_token = find_response_json['accessToken']
        return 'http://localhost:3000/public-dashboards/' + find_access_token

    # first time, create public dashboard
    payload = {
        "uid": PUBLIC_DASHBOARD_UID,
        "timeSelectionEnabled": True,
        "isEnabled": True,
        "annotationsEnabled": False,
        "share": "public"
    }
    response = requests.post(url=endpoint, json=payload)
    json_response = response.json()
    access_token = json_response['accessToken']
    embed_url = 'http://localhost:3000/public-dashboards/' + access_token
