## HW 3 - Kubernetes
### Description: 
Following the results from the previous exercise, we will start orchestrating Network Policies and nginx application a little more. We will try and achieve, described the following **Task Goals:** 
* Create more pods to single namespace.
* Create a network policy that will block the **single** pod from all other pods.
  * Ensure you query the blocked pod using pod's hostname and IP address.  
* Create NGINX Controller.
* Forward routes to /[xyz] to the deployment in the [xyz] namespace. ***Note: /xyz is route***
* --Do I need to do this? (Matt to confirm)
  * Build an ingress **gateway** to both **services** you have deployed. 
  * Add self-signed certificate for TLS. 

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
1) Creating Pod: 
  ```bash
  kubectl run [PodName] --image=[image]:[tag] --port=[port no.] -n [namespace_name] --dry-run=[client | server | none] -o yaml > [fileName].yaml
  ```

  Then you will get the following file: 
  ```yaml
  apiVersion: v1
  kind: Pod
  metadata:
    labels:
      app: [podLabel]
    name: [podName]
    namespace: [namespace_name]
  spec:
    containers:
    - image: [image]:[tag]
      name: [containerName]
      ports:
      - containerPort: [portNo.]
      resources:
        requests:
          cpu: ["00m"] #Min micro processors to run container
          memory: ["00Mi"] #Min MiB to run container
        limits:
          cpu: ["00m"] #Max micro processors to run container
          memory: ["00Mi"] #Max MiB to run container
    dnsPolicy: ClusterFirst
    restartPolicy: Always
  status: {}
  ```
  Then to apply the above yaml file, you run the below command: 
  ```bash
  kubectl apply -f [fileName].yaml
  ```

2) Create a network policy that will block the **single** pod from all other pods.
To perform this part of this exercise, you need to hardcode your yaml script. However the kubernetes [documentation](https://kubernetes.io/docs/concepts/services-networking/network-policies/) covering Network Policies will come in handy! 

It is also important to understand [subnetting](https://docs.netgate.com/pfsense/en/latest/network/cidr.html), ensuring how many pods in the namespace you need to block. 

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: [specify policy]
  namespace: [namespace_name]
spec:
  podSelector:
    matchLabels:
      app: [podLabel]
  ingress:
    - from:
      - ipBlock:
          cidr: [IP Address]/32 # Setting subnet to 32, will restrict to only single pod.
      - namespaceSelector:
          matchLabels: [namespace] # You are defining a namespace, which you will allowing pods talking in different namespaces.
      - podSelector:
          matchLabels:
            app: [podLabel] # You are defining the pod which is allowing to talk to the specific pod, and you may need to include namespace name if the pod is to a different namespace.
      ports:
        - protocol: # protocol: i.e. TCP or UDP
          port: [portNo.]
  policyTypes:
    - Ingress
```
When done the above, you then will run the kubectl command to apply the network policy: 
```bash
kubectl apply -f [fileName].yaml
```
Now, say you have the following running on your kubernetes:
- fruit
  - apple
  - banana
  - grapes
- food
  - pasta
  - chicken

Let's apply the above Network Policies to **grapes** pod, given the example above. <br/>
When the Network Policy has been applied, we then be able to query **grapes** pod from any pod. The result expected, should timeout. 
```shell
> kubectl exec -n fruit grapes -- curl -m1 [svc_name].food.svc.cluster.local
> % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                  Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:--  0:00:01 --:--:--     0
  curl: (28) Connection timed out after 1002 milliseconds
  command terminated with exit code 28
```
Also, a successfull should look like the following:
```shell
> kubectl exec -n fruit banana -- curl -m1 [svc_name].food.svc.cluster.local
> % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                  Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0<!DOCTYPE html>
  <html>
  <head>
...
  </html>
  100   615  100   615    0     0  76875      0 --:--:-- --:--:-- --:--:-- 76875
```

3) Now, lets create a local image and run it on kubernetes (minikube). Example, we have created a html page (index.html) and a Dockerfile. 
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
4) 