import requests
import json

resp = requests.post("http://photostyleanalysis.ddns.net/psa-controller/predict", headers={'X-API-KEY':'**********'}, files = {"file": open('/home/mike/Artificial Intelligence MSc/3rd Semester/Thesis/cat.jpg', 'rb')})
print(resp.json())
