![alt text](https://i.imgur.com/68Juvpa.png)

# Thesis: Photography Style Analysis

This repo contains work for my Thesis at the MSc Program of AI 2020-2022, organized by NCSR Demokritos and University of Piraeus.

Domain: http://photostyleanalysis.ddns.net/

Supervisor: Mr. Theodoros Giannakopoulos - [tygiannak](https://github.com/tyiannak)

## Documentation

### API

Ways to access the API:

* Swagger UI
* Postman
* curl
* Script (bash/python/js)

#### Examples

[/psa-controller/predict](http://photostyleanalysis.ddns.net/psa-controller/predict) (*given an image, try and predict its main subject*):

* **via Swagger:**

![alt text](https://i.imgur.com/DrzHENN.png)

* **via Postman:**

![alt text](https://i.imgur.com/WkGvYIc.png)

* **via curl:**

*curl -X POST http://<!--This is a comment-->photostyleanalysis.ddns.net/<!--This is a comment-->psa-controller/predict -F "file=@/path/to/image"*

![alt text](https://i.imgur.com/J1fof8w.png)

* **via Python Script:** 

[example](https://github.com/mzouros/MSc_AI_thesis/blob/main/postReq.py)
