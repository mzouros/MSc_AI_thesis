import requests
import json

resp = requests.post("http://photostyleanalysis.ddns.net/psa-controller/predict", files = {"file": open('/path/to/image', 'rb')})
print(resp.json())
