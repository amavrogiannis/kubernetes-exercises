## HW 2 - Kubernetes
**Task Goal:** 
* Create 2 namespaces.
* Create 1 deployment to each namespace containing 1 pod.
* Create service for each deployment (**not LoadBalancer**)
* Each pod is able to communicate with your service via: 
    * IP Address
    * Hostname

Key articles: 
* [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
* [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)

**Pre-requisits setup**
Install **minikube** and run the following: <br/>
```bash
minikube start --network-plugin=cni
```

Then, to setup calico on your minikube, follow the instructions **[here](https://projectcalico.docs.tigera.io/getting-started/kubernetes/minikube#create-a-single-node-minikube-cluster)**. <br/>
The reason why we are using calico, is to challenge with kubernetes networks and network security on minikube. Which is also equivilently set up in any cloud provider Kubernetes services. (EKS, AKS and GKE).

**Exercise below:**
1) Creating namespaces: 
    ```bash 
    kubectl create ns [namespace name]
    ```

2) Creating deployment using dry-run and output deployment to a yaml file:
    ```bash
    kubectl create deployment [deployment name] -n [namespace name] --image=[image:tag] --port=[port no.] --dry-run=[client | server | none] -o yaml > [file name].yaml
    ```
    Then, --dry-run feature will not initiate the cluster building a deployment and will only generate the file for your to apply afterwards. 
    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
    labels:
        app: [deployment name]
    name: [deployment name]
    namespace: [namespace name]
    spec:
    replicas: 1
    selector:
        matchLabels:
        app: [deployment name]
    strategy: {}
    template:
        metadata:
        labels:
            app: [deployment name]
        spec:
        containers:
        - image: [container]:[tag]
            name: [container name]
            ports:
            - containerPort: 80
            resources:
            requests:
                cpu: "30m"
                memory: "50Mi"
            limits:
                cpu: "100m"
                memory: "150Mi"
    status: {}
    ```
    Later, you will be able to run your yaml file, after you applied your changes: 
    ```bash
    kubectl apply -f [file name].yaml
    ```

3) Running below command to create a service: 
    ```bash
    kubectl create service clusterip [svc name] --namespace=[ns name] --tcp=[port no.]:[target no.] --dry-run=[client | server | none] -o yaml > [file name].yaml
    ```
    Then, cluster IP service will generate the following yaml for you: 
    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
    labels:
        app: [service name]
    name: [service name]
    namespace: [namespace name]
    spec:
    ports:
    - name: 8080-80
        port: [port number]
        protocol: TCP
        targetPort: [target port number]
    selector:
        app: [deployment name] # Change to your deployment name here.
    type: ClusterIP
    status:
    loadBalancer: {}
    ```

    To apply, simply run: 
    ```bash
    kubectl apply -f [file name].yaml
    ```

4) To query across pod to service to different workspaces, you need the `exec` feature. 
But so far, we have the following: 
---
* Namespace: fruits
    * Deployment: apple
        * Pods: 1
    * Service: tree
        * Type: ClusterIP
---
* Namespace: liquid
    * Deployment: water
        * Pods: 1
    * Service: weather
        * Type: ClusterIP
---
Which in this case, you will have to run the following on your command line: 
```command
kubectl -n [namespace] exec [pod_name] -- curl -m 1 [service name].[namespace].svc.cluster.local:[port_number]
```

You should get a respoce as follows: 
```command
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
...
<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

6) **Optional task:** Block inbound/outbound communication between services using Network Policies. <br/>
    a) Having you setup calico, you can use Network Policies on your minikube. <br/> <br/>
**Description** <br/>
It is good practice for you to understand how [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) work in Kubernetes, so you can be able to protect pods that host sensitive data and restricting other pods from accessing. To do that, you need to hardcode the yaml script 😢.

To block all access from all pods from your particular namespace, the yaml file should look like: 
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all # Name of the Policy.
  namespace: [namespace_name] 
spec:
  podSelector: {} # This applies to any Pod inside the namespace.
  policyTypes: # You are applying the policy to block inbound/outbound traffic. 
    - Ingress
    - Egress
```

You can still configure other behaviours such as: 
- **Allow inbound** Traffic: 
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-all-ingress
spec:
  podSelector: {}
  ingress: #You allow all inbound traffic 
  - {}
  policyTypes:
  - Ingress
```
- **Block inbound** Traffic:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
spec:
  podSelector: {}
  policyTypes:
  - Ingress
```
As you realise, the only difference between the two. You will need to add `ingress` to your script, so Kubernetes can understand you are allowing all traffic. 

Now, for **outbound** traffic: 
- **Allow oubound** Traffic: 
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-all-egress
spec:
  podSelector: {}
  ingress: #You allow all outbound traffic 
  - {}
  policyTypes:
  - Egress
```
- **Block outbound** Traffic:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-egress
spec:
  podSelector: {}
  policyTypes:
  - Egress
```
---
If you have any questions, please ask away.