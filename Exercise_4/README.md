## HW 4 - Kubernetes
### Description: 
1. Create a secret with keys
    - example: 
      - username: bob
      - password: mypassword
2. apply the secret as an environmental vairable to your pod
3. expose the secrets username in the html
4. Create an ingress to 2 of your service in different namespaces
5. Update your localhost to example.com  and point to the IP of the ingress
6. Create a self signed TLS cert with example.com as the CN
7. Apply the TLS to the ingress controller


Key articles: 
* [cert-manager](https://cert-manager.io/docs/)
* [https ingress controller](https://www.civo.com/learn/kubernetes-https-ingress-controller-with-your-own-tls-certificate)

---
### Pre-requisits setup:
Install **minikube** and run the following: <br/>
```bash
minikube start --network-plugin=cni
```

Then, to setup calico on your minikube, follow the instructions **[here](https://projectcalico.docs.tigera.io/getting-started/kubernetes/minikube#create-a-single-node-minikube-cluster)**. <br/>
The reason why we are using calico, is to challenge with kubernetes networks and network security on minikube. Which is also equivilently set up in any cloud provider Kubernetes services. (EKS, AKS and GKE).
<br><br>
**NEW:** You will need a web application, for pulling environmental variables using the container inside the Pod. 

---
**Exercise below:**

1) Secret in kubernetes is a way to save your keys within your cluster securely and apply to your deployments/pods where your application container may find useful in accessing databases, pushing specific values on your webapp and so on. 
<br>
To get our hands dirty, here is the practice demo: 
```yaml
filename: fakeSecret.yaml

apiVersion: v1
kind: Secret
metadata:
  name: fake-secret
  namespace: fruits
type: Opaque
data:
  TV_ENV: dGhlX25vdGVib29rCg==
```

TV_ENV is an environment. Kubernetes will require you to encode the secret using base64. 
```bash
echo "Your_String_Values" | base64
```

But the values to this encoding, we typed: **the_notebook**
<br> 
Then we deploy the secret, running the following. 
```bash
kubectl apply -f fakeSecret.yaml
```

2) Kubernetes will confirm the secret and now, you need to apply it on your deploy it, so our Flask application is going to pull the env variable: 
```yaml
filename: kubeDeployment.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: apple
    store: supermarket
  name: apple
  namespace: fruits
spec:
  replicas: 1
  selector:
    matchLabels:
      app: apple
  template:
    metadata:
      labels:
        app: apple
        store: supermarket
    spec:
      containers:
      - image: flask_app:v2
        name: flask
        ports:
        - containerPort: 5000
        resources: {}
        env:
          - name: TV_ENV # Applying the env variable that the container is going to use
            valueFrom:
              secretKeyRef:
                name: fake-secret # Name of the secret
                key: TV_ENV # The key, which is specified from the secrets. 
      volumes: # Yes, you need to attach the secret as a volume. 
        - name: secret-env # Name your secret
          secret: 
            secretName: fake-secret # That is the secret resource name you specified on secrets file. 
```
To apply, run `kubectl apply -f kubeDeployment.yaml` and should apply your secrets. 

3) As following instructions, we are using the Flask application to pull the environmental variables, which is stored on /cont_image folder. This is where you are able to use `docker build` to create your container. 
<br>
The container name: `flask_app:v2`
<br> 
The flask application is pulling `TV_ENV` from the system and pushes it to the web application html file, so then appears when it operates.

More details shown on `/cont_image/README.md`

4) This exercise applies back to what we achieved with Exercise 3. The only difference in this Exercise 4, we are using Flask to run our application and is using port 5000. Please, ensure your service follows the example below: 
```yaml 
apiVersion: v1
kind: Service
metadata:
  labels:
    store: supermarket
  name: fruiteria
  namespace: fruits
spec:
  ports:
  - port: 8080 # port_number_expose
    protocol: TCP
    targetPort: 5000
  selector:
    store: supermarket
  type: NodePort
```
5) To give a domain on your localhost, you need to add the following fields for `example.com`. 
```bash
sudo nano /etc/hosts
```
Add the following line on the file and save: 
```bash
127.0.0.1 example.com
```
And then, you will see your application operating on your localhost, can now use the local set domain `example.com`.

6) To perform this task, first you need to create self-signed certificate. Make sure you remember example.com domain: 
    - Create a folder and go inside it. Make sure you have `openssl` installed. 
Execute the following `openssl` command to create the `rootCA.key` and `rootCA.crt`. Replace `example.com` with your domain name or IP address
```bash
openssl req -x509 \
            -sha256 -days 356 \
            -nodes \
            -newkey rsa:2048 \
            -subj "/CN=example.com/C=UK/L=London" \
            -keyout rootCA.key -out rootCA.crt 
```
a) Create the server private key
```bash
openssl genrsa -out server.key 2048
```
b) Create Certificate Signing Request Configuration
```basg
cat > csr.conf <<EOF

[ req ]
default_bits = 2048
prompt = no
default_md = sha256
req_extensions = req_ext
distinguished_name = dn

[ dn ]
C = UK
ST = London
L = London
O = testlabs
OU = test lab
CN = example.com

[ req_ext ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = example.com
EOF
```
c) Generate Certificate Signing Request (CSR) Using Server Private Key
```bash
openssl req -new -key server.key -out server.csr -config csr.conf
```
d) Create a external file
```bash
cat > cert.conf <<EOF

authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = example.com

EOF
```

To apply the secrets on Kubernetes, run the following: 
```bash
kubectl create secret tls example-local --cert=server.crt --key=server.key --dry-run=client -o yaml > tls-secret.yaml 
```
Then open `tls-secret.yaml` to modify: 
```yaml
apiVersion: v1
kind: Secret
type: kubernetes.io/tls
data:
  tls.crt: [tls cert file imported in base64]
  tls.key: [tls key file imported in base64]
metadata:
  name: example-local
  namespace: fruits
```
Finally, apply the file to create secret. 
7) To apply the TLS secret on your ingress, you need to create a new section as shown here: 
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: supermarket-ingress
  namespace: fruits
  labels:
    service: application-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  tls: # applying tls secret
    - hosts: 
        - example.com #domain applied on hosts file
      secretName: example-local # secret stored in cluster
  rules:
  - host: example.com
    http:
      paths:
      - path: /fruits
        pathType: Prefix
        backend:
          service:
            name: fruiteria 
            port:
              number: 8080
```
Finally, you will be able to view the content on your localhost with port `443`. 
