# Flask IP app
## About
Web app designed to return an IP address of requesting client or list of IP's that queried the app in the past. Dockerized and ready for deployment on Kubernetes or Openshift. For storage I went with Redis.

## Description
This project is nothing more than a Flask app that runs on port `5000` with two main API endpoints: 

```/get-ip``` - returns an IP address of requesting client

```/get-ip-list``` - returns a list of IP addresses that have queried the app in the past

There is also a third endpoint - ```/health-check``` - it was specifically made for livenessProbe done by k8s and doesn't provide any functionality.

Those IP addresses are stored in Redis, which is used as primary storage, in form of a set with unique records. Redis deployment isn't a proper production-grade Redis cluster with master, replication, etc. it's just a simple pod deployment without any additional configuration - the app is basic and not aimed for production purposes, thus made this way. Features like basic event logging and exception handling were implemented too.

Accept headers in HTTP request are respected and based on received header, different formats will be returned. For any unsupported format, the response will be in `text/plain` 

Supported formats are:
- **xml**  - `text/xml`, `application/xml`
- **html** - `text/yaml`, `text/x-yaml`, `application/x-yaml`
- **yaml** - `text/html`
- **txt**  - `text/plain`

App supports rate limiting per client IP address - it is set by default to **15 requests per minute** for all endpoints.

## Prerequisites
Personally, I run and tested the app on `minikube`. If you don't have a proper cluster at your disposal, I suggest to [set up minikube](https://minikube.sigs.k8s.io/docs/start/) as it is probably the fastest way to get it running.

## How to deploy and access?
Assuming you have `minikube` installed and you are at the root level of repo, all that has to be done is:
```
minikube start
minikube kubectl apply -f deployment/minikube/
```
This will create **NodePort** and **LoadBalancer** services that can help you access the deployment.

---
To access via **NodePort** run this command in seperate terminal and let it run for the time of using the app:
```
minikube service flask-app -n ip-app --url
```

Use given address to access the app.

---
For access using **LoadBalancer**, run in seperate terminal and also leave running:
```
minikube tunnel
```
After that go to another terminal and type:
```
kubectl get svc flask-app-lb -n ip-app
```
Copy the EXTERNAL-IP and add application port at the end:
```
http://EXTERNAL_IP:5000
```
---

## What will be deployed?
When deploying on `minikube`:
- `ip-app namespace` - every other resource will be created there
- `redis deployment` - Redis deployment with 1 initial replica
- `redis service` - headless service of ClusterIP type on Redis port - `6379`
- `app configmap` - configuration variables for Flask to connect with Redis
- `app deployment` - Flask app deployment with 1 initial replica
- `app service` - service of NodePort type - port is set to `32123`
- `app load balancer service`* - service of LoadBalancer type running on port `5000` 

*The last one, LoadBalancer is specific to `minikube` - it provides this functionality so I decided to use it additionally. Other deployment manifests are stripped off of it (well, unless you want to run it in the cloud, then you can use it).

Other directories in [/deployment](./deployment) contain roughly the same manifests for Openshift and Kubernetes without the LoadBalancer.

## Optimizing Docker image
By using multi-stage build and distroless **python3** image in [Dockerfile](./src/Dockerfile), I managed to drop down the size of the image down to 76.1MB
```
REPOSITORY                    TAG       IMAGE ID       CREATED        SIZE
kxpic/ip-app                  latest    3d14a3cbbcdd   14 hours ago   76.1MB
```

## Issues, notes, thoughts
- For Openshift, I could probably use Route as a way to access the app - unfortunatelly I didn't have the proper environment so I didn't want use it just because 'I think it will work'. Access using NodePort will still work fine though.

- As of this commit, my readinessProbe and livenessProbe for Flask fail with 404 code when using ```/health-check``` endpoint, but work for other ones. I tried rebuilding it with no-cache option to make sure latest changes are on the image but it didn't help.
