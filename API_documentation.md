<p align="center">
  <img src="https://i.imgur.com/68Juvpa.png"/>
</p>


### API Documentation

Ways to access the API:

* Swagger UI
* Postman
* curl
* Script (bash/python/js)

#### Examples

[/psa-controller/predict](http://photostyleanalysis.ddns.net/psa-controller/predict) (*given an image, try and predict its main subject*):

* **via Swagger:**

  * **Authorization:**
![alt text](https://i.imgur.com/Dvu0ld5.png)
![alt text](https://i.imgur.com/Y4u2kij.png)

  * **Execute:**
![alt text](https://i.imgur.com/nfImlFs.png)

* **via Postman:**

  * **Body:**
![alt text](https://i.imgur.com/PxGVSwk.png)

  * **Authorization:**
![alt text](https://i.imgur.com/txXeZR1.png)

* **via curl:**

*curl -X POST http://<!--This is a comment-->photostyleanalysis.ddns.net/<!--This is a comment-->psa-controller/predict -H "X-API-KEY:***********" -F "file=@/path/to/image"*

![alt text](https://i.imgur.com/2qc4LGg.png)

* **via Python Script:** 

[example](https://github.com/mzouros/MSc_AI_thesis/blob/main/postReq.py)
