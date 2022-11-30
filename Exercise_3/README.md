## HW 3 - Kubernetes
### Description: 
Following the results from the previous exercise, we will start orchestrating Network Policies and nginx application a little more. We will try and achieve, described the following **Task Goals:** 
* Build diffrent container Applications using `docker build`. 
* Create K8s managed ingress controller.
* Forward routes to /[xyz] to the deployment in the [xyz] namespace. ***Note: /xyz is route***


Key articles: 
* [Nginx Ingress Controller](https://docs.nginx.com/nginx-ingress-controller/intro/overview/)

---
### Pre-requisits setup:
Install **minikube** and run the following: <br/>
```bash
minikube start --network-plugin=cni
```

Then, to setup calico on your minikube, follow the instructions **[here](https://projectcalico.docs.tigera.io/getting-started/kubernetes/minikube#create-a-single-node-minikube-cluster)**. <br/>
The reason why we are using calico, is to challenge with kubernetes networks and network security on minikube. Which is also equivilently set up in any cloud provider Kubernetes services. (EKS, AKS and GKE).

---
**Exercise below:**

1) Creating a local image and run it on kubernetes (minikube). Example, we have created a html page (index.html) and a Dockerfile. 
```html
<!DOCTYPE html>
<html>
<body>

<h1>Hey hey v2</h1>
<h2>this nginx is running on:</h2>

<p id="demo"></p>

<script>
let hostname = location.hostname;
document.getElementById("demo").innerHTML = hostname;
</script>

<h3 style="color:Blue;">London is Blue</h3>

</body>
</html>
```
```Dockerfile
FROM nginx:alpine

COPY ./index.html /usr/share/nginx/html

EXPOSE 80
```
To build the image, you need to run the `docker build` command, below: 
```command
docker build . -t [image_name]:[tag/version]
```
To to use the image on your `minikube`, run the following command: 
```command
minikube image load [image_name]:[tag/version]
```
2) 