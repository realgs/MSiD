import urllib.request, json

def get_json_data(url):
    with urllib.request.urlopen(url) as u:
        return json.loads(u.read().decode())
