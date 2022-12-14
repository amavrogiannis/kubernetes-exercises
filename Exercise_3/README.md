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
2) Next, we will use the containers we pushed on minikube, so we can access our application as a path to our local domain. (i.e. example.com/path). We will be using Ingress, where kubernetes is going to forward to the application, using the specified domain path.
To do so, we will deploy the following: 
    - Application
    - Service
    - Ingress
- Please note: *In order for it to work, you will need to enable `minikube tunnel`*. i had to enable special privileges for it to make it work at times `sudo minikube tunnel`.
**Bringing the Action**
- Install Ingress Controller: 
    - Run the manifest to install Ingress: `kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.5.1/deploy/static/provider/cloud/deploy.yaml` as documented in the [documentation](https://kubernetes.github.io/ingress-nginx/deploy/).
- Create the following: 
    - Run your application deployment with --port=80 and then create `NodePort` service on the same namespace, you deployed your app. 
    - Create your Ingress yaml file. `kubectl create ingress fruits-ingress -n league --rule host/path=football-svc:12500 --dry-run=client -o yaml > ingress.yaml`.
    - Modify the following values, which you will direct your application to a path. 
```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: [ingress service name] # name your ingress
  namespace: [namespace name] # Use the same namespace, as you are using your app. 
  labels:
    service: [ingress service name] # Tag your ingress 
  annotations: # This section is for specific ingress objects, for you to customise their behavious. For this case, we use the below. 
    kubernetes.io/ingress.class: nginx # We classify this application is running on nginx.  
    nginx.ingress.kubernetes.io/rewrite-target: / # If you are setting up a path, good for k8s knowing you want your application to be routed there. 
spec:
  rules:
  - host: [domain_name] # If you have a domain that your app is going to be published from, add its domain name. If you set it to your local env. specify localhost.
    http:
      paths:
      - path: /[path] # You define the path name. i.e. for yoga.com/page you write it as /page
        pathType: Prefix
        backend:
          service:
            name: [service_name] # You need to specify the service name you are using to expose your app. 
            port:
              number: [port_number] # Enter the port number your service is exposed to.

```
- references: 
    - annotations: https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/ 
3) Run `kubectl apply -f ingress.yaml` *(Please, ensure you have minikube tunner enabled.)*. Then you should be able to check your browser in the URL: http://localhost/[path]