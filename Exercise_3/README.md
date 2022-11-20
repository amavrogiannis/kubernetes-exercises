## HW 3 - Kubernetes
### Description: 
Following the results from the previous exercise, we will start orchestrating Network Policies and nginx application a little more. We will try and achieve, described the following **Task Goals:** 
* Create more pods to single namespace.
* Create a network policy that will block the **single** pod from all other pods.
    * Ensure you query the blocked pod using pod's hostname and IP address.  
* Install an ingress class of type nginx.
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
