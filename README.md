WheelAppeal
===================
This repository contains the code for the WheelAppeal mobile app, REST api, and website. This document will explain the usage of each component. First, clone the repository:

```
git clone https://github.com/tomplarge/wheelappeal.git
```
----------


Mobile App
-------------
You must have the following requirements:
- Xcode (latest version)
- React Native (see 'Building Projects with Native Code' at <href> <href> https://facebook.github.io/react-native/docs/getting-started.html </href>)

To run, do the following:
```
cd wheelappeal/mobile_app
react-native run-ios
```

This should start up a terminal window for the JS development server and an iPhone simulator containing the mobile app.

REST API -- OBSOLETE
----------
The REST Api is used for querying our MySQL database for food truck data. Currently, the API can be reached by a GET request at the following address:
```
ec2-13-59-2-226.us-east-2.compute.amazonaws.com/v1/menu
```

This API currently utilizes Docker as a container for the API and gunicorn as an HTTP server.

To run the API, you must have the following requirements:
- Docker (see <href> https://docs.docker.com/engine/installation/ </href>)

To run, be sure the docker daemon is running and do the following:
```
cd wheelappeal/api
docker build -t api .
docker run -d -p 80:5000 api
```
You should see messages indicating the docker container is running with the api. To confirm, open up another terminal window and run:
```
docker ps
```

You should see the container you just started as a running process. Then, to confirm the api is reachable, run:
```
curl localhost/v1/menu
```
You should see text returned.

Website -- Transitioning REST API here
----------
The website currently holds information about WheelAppeal at <href> http://www.wheelappeal.co </href>. The API is currently hosted as well at <href> http://www.wheelappeal.co/api </href>

If you are starting up the server, you must have the following prerequisites:
- (Optional) Docker (see <href> https://docs.docker.com/engine/installation/ </href>)
- Django (see <href> https://docs.djangoproject.com/en/1.11/topics/install/ </href>)
- (Optional) Nginx (see <href> https://www.nginx.com/resources/wiki/start/topics/tutorials/install/ </href>)

First, change into the website directory
```
cd wheelappeal/website
```
To run locally with Docker (and gunicorn):
```
docker buld -t web .
docker run -d -p 8000:8000
```
To run locally with Django:
```
python manage.py runserver
```

Paste the address below into a web browser to confirm:

```
localhost:8000
```

To run on an EC2 instance  do the following:
- Add the IP address and 127.0.0.1 to ALLOWED_HOSTS array in settings.py
```
vim website/settings.py
```
- Copy the nginx.conf file to nginx directory
```
sudo cp website/nginx.conf /etc/nginx/nginx.conf
```
- Start nginx
```
service nginx start
```
- Build Docker image
```
docker build -t web .
docker run -d -p 8000:8000 web
```
- Go to the IP address of the instance in a web browser to confirm. Alternatively, run:
```
curl 127.0.0.1
```
