# Notify API
## This API runs integrated with a Postgress!!

it have thre methods:

_POST - saves one message on the data-base_

_PUT - Updates the read flag on the data-base_

_GET - Get all messages from one destination_


## Step One! 
### Prepare your Environment with Minikube!



To install minikube use: [minikube oficial docs](https://minikube.sigs.k8s.io/docs/start/)

after install... Let's start k8s with the following commands:

```
$ minikube start --driver=docker
```

```
$ minikube addons enable metallb
```

```
$ minikube addons configure metallb

-- Enter Load Balancer Start IP: 192.168.49.100
-- Enter Load Balancer End IP: 192.168.49.120
     Using image metallb/speaker:v0.9.6
     Using image metallb/controller:v0.9.6
  metallb was successfully configured
```

Reference [doc](https://docs.epinio.io/howtos/) to start _minikube_.

## Install epinio on minikube
The Epinio need two resouces to works, first: one _ingress-control_ and one _cert-manager_.

  In order to install _ingress-control_ use:

```
$ minikube addons enable ingress
```
read the oficial [doc](https://kubernetes.github.io/ingress-nginx/deploy/#minikube) for more details.

  


For _certManager_:
```
$ kubectl create namespace cert-manager
$ helm repo add jetstack https://charts.jetstack.io
$ helm repo update
$ helm install cert-manager --namespace cert-manager jetstack/cert-manager \
        --set installCRDs=true \
        --set "extraArgs[0]=--enable-certificate-owner-ref=true"
```

### After all steps above your cluster is ready to deploy epinio!!!

So let's use the helm to do it!!
```
$ helm repo add epinio https://epinio.github.io/helm-charts
```
Here! We have that to provide one global domain. As our env is a developer environment, no problem in use one magic-domain for it!

exemple: 
```
192-168-49-100.sslip.io
```
So we set it.
```
$ helm install epinio -n epinio --create-namespace epinio/epinio --set global.domain=192-168-49-100.sslip.io
```

Good Job!! Now we need to install the epinio-cli! For it let's do: 
```
$ curl -o epinio -L https://github.com/epinio/epinio/releases/download/v1.5.0/epinio-linux-x86_64
```
```
$ chmod +x epinio
```
```
$ sudo mv ./epinio /usr/local/bin/epinio
```
In order to test, use:
```
> epinio version
Epinio Version: v1.5.0
Go Version: go1.18
```
That's great!!!

Due we use one magic-domain we need modify our ```/etc/hosts```
 , but no worries this step is very simple!!
```
sudo echo "192.168.49.2  'https://epinio.192-168-49-100.sslip.io" >> /etc/hosts
```


Now let's do the last command, this step able to use epinio!!

```
epinio login -u admin 'https://epinio.192-168-49-100.sslip.io'
```

Trust the certificate by pressing ```'y'``` and ```'enter'```

The default password is _"password"_. So use: 
```
$ epinio settings show
```
to verify if everything has running very well
# Deploy app with Epinio

first we are deploy one database service. 
```
$ epinio service create postgresql-dev my-postgres
```

We can list all services deployed using:
```
$ epinio service list
```
Now let's deploy our application!!!!

inside the app path use:
```
epinio push --name not-api  --path ../notifications_api
```

### That's It. Thank you for reading!!
