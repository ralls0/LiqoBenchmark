# Liqo benchmark

## Table of Contents

1. [Intro](#intro)
2. [Provision the playground](#provision-the-playground)
    1. [Docker](#docker)
    2. [Kind & kubectl](#kind--kubectl)
    3. [Helm](#helm)
3. [Test](#test)
4. [Test 1](#test-1)
    1. [Creation of the Cluster](#creation-of-the-cluster)
    2. [Deploy of the application](#deploy-of-the-application)
    3. [Prometheus and Locust exporter](#prometheus-and-locust-exporter)
    4. [Deploying the Kubernetes Metrics Server on a Cluster Using Kubectl](#deploying-the-kubernetes-metrics-server-on-a-cluster-using-kubectl)
    5. [HPA - Horizontal Pod Autoscaling](#hpa---horizontal-pod-autoscaling)
5. [Test 2](#test-2)
    1. [Creation of the Cluster](#creation-of-the-cluster-1)
    2. [Liqo installation](#liqo-installation)
    3. [Deploy of the application](#deploy-of-the-application-1)
    4. [Prometheus and Locust exporter](#prometheus-and-locust-exporter-1)
    5. [Deploying the Kubernetes Metrics Server on a Cluster Using Kubectl](#deploying-the-kubernetes-metrics-server-on-a-cluster-using-kubectl-1)
    6. [HPA - Horizontal Pod Autoscaling](#hpa---horizontal-pod-autoscaling-1)
6. [Test 3](#test-3)
    1. [Creation of the Cluster](#creation-of-the-cluster-2)
    2. [Liqo installation](#liqo-installation)
    3. [Linkerd installation](#linkerd-installation)
    4. [Deploy of the application](#deploy-of-the-application-2)
    5. [Prometheus and Locust exporter](#prometheus-and-locust-exporter-2)
    6. [Deploying the Kubernetes Metrics Server on a Cluster Using Kubectl](#deploying-the-kubernetes-metrics-server-on-a-cluster-using-kubectl-2)
    7. [HPA - Horizontal Pod Autoscaling](#hpa---horizontal-pod-autoscaling-2)
7. [Test 4](#test-4)
    1. [Creation of the Cluster](#creation-of-the-cluster-3)
    2. [Deploy of the MetalLB](#deploy-of-the-metallb)
    3. [Creation of the trust anchor](#creation-of-the-trust-anchor)
    4. [Linkerd installation](#linkerd-installation-1)
    5. [Deploy of the application](#deploy-of-the-application-3)
    6. [Prometheus and Locust exporter](#prometheus-and-locust-exporter-3)
    7. [Deploying the Kubernetes Metrics Server on a Cluster Using Kubectl](#deploying-the-kubernetes-metrics-server-on-a-cluster-using-kubectl-3)
    8. [HPA - Horizontal Pod Autoscaling](#hpa---horizontal-pod-autoscaling-3)

## Intro

Nowadays more and more enterprises use and orchestrate more than one cloud platform to deliver application services. In this context it is born "The Liqo project", which enables the creation of a multi-cluster environment. Moreover, the Service Mesh is a new technology that is being developed. It provides features like observability, reliability, security, and even a better Load Balancing than Kubernetes ones. This project aims at simulating a real scenario where a micro-services application like [Online Boutique](https://github.com/GoogleCloudPlatform/microservices-demo) provided by Google, which includes multiple cooperating services, wants to scale based on the workloads reached into the cluster and on more clusters. During the project, you'll design, setup, implement and compare different scenarios and service mesh solutions like Service Mesh on Liqo or Linkerd.

## Provision the playground

Before starting to run the demos you should have installed some software on your system.

For my tests, I’m going to setup the clusters on the virtual machines hosted on [CrownLabs](https://crownlabs.polito.it/).

> VMs: Ubuntu Desktop 20.04 with 8 CORE, 8 GB of RAM, and 50 GB of disk.
> NOTE: By default, not all 25 GB are available. You can use these commands to extend the disk:

```bash
sudo growpart /dev/vda 2
sudo growpart /dev/vda 5
sudo resize2fs /dev/vda5
```

First things first, I'm going to install some extra tools, and all the necessary dependencies on all the VMs:

```bash
sudo apt update
sudo apt install -y apt-transport-https  ca-certificates curl gnupg lsb-release xclip git jq

# Goland
wget https://go.dev/dl/go1.18.linux-amd64.tar.gz
sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.18.linux-amd64.tar.gz

# Step
wget https://dl.step.sm/gh-release/cli/docs-cli-install/v0.19.0/step-cli_0.19.0_amd64.deb
sudo dpkg -i step-cli_0.19.0_amd64.deb
```

Now, you can check and install all the necessary software for the system:

### Docker

```bash
# Check
command -v docker

# Install
sudo apt update
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io
```

### Kind & kubectl

```bash
# Check
command -v kind

# Install
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.11.1/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/bin/kind

#Check
command -v kubectl

# Install
sudo apt update
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt update
sudo apt install -y kubectl
sudo apt-mark hold kubectl
```

### Helm

Finally, helm because the `liqoctl` uses it to configure and install the Liqo by means of `helm chart`.

```bash
# Check
command -v helm

# Install
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```

## Test

For these tests, you'll play with a [micro-services application provided by Google](https://github.com/GoogleCloudPlatform/microservices-demo), which includes multiple cooperating services. Four different scenarios are provided:

1. Online Boutique on a basic cluster.
2. Online Boutique on a multi-cluster with Liqo.
3. Online Boutique on a multi-cluster with Liqo, and Linkerd as Service Mesh provider.
4. Online Boutique on a multi-cluster with Linkerd.

## Test 1

### Creation of the Cluster

Before starting the test, you should create the cluster where you'll operate.

```bash
# Test 1
sudo kind create cluster --name cluster1 --kubeconfig $HOME/.kube/configC1 --image kindest/node:v1.23.5
sudo chmod 644 $HOME/.kube/configC1
echo "alias lc1=\"export KUBECONFIG=$HOME/.kube/configC1\"" >> $HOME/.bashrc

source $HOME/.bashrc
lc1
```

### Deploy of the application

```bash
k create ns online-boutique
k apply -f ./kubernetes-manifests/online-boutique/boutique-manifests.yaml -n online-boutique
```

Once the demo application manifest is applied, you can observe the creation of the different pods:

```bash
k get pods -n online-boutique -o wide
```

And with the command `kubectl port-forward` you can forward the requests from your local machine (i.e. `http://localhost:8080`) to the frontend service:

```bash
kubectl port-forward -n online-boutique service/frontend-external 8080:80
```

Before deploying the kube-prometheus stack you must start the loadgenerator.

```bash
kubectl port-forward -n online-boutique service/loadgenerator 8089
```

I'm using 200 users with 1 second of spawn rate for my test.

Now, you can check that losut-exporter is monitoring the loadgenerator resource.

```bash
kubectl port-forward -n online-boutique service/locust-exporter 9646
```

### Prometheus and Locust exporter

Before setting up a monitoring system with Grafana and Prometheus, you’ll first deploy the kube-prometheus stack Helm chart. The stack contains Prometheus, Grafana, Alertmanager, Prometheus operator, and other monitoring resources.

```bash
kubectl create namespace monitoring

# Add prometheus-community repo and update
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts && helm repo update

# Install
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring
```

Finally, run the following command to confirm your kube-prometheus stack deployment.

```bash
kubectl get pods -n monitoring
```

You’ll use the Prometheus service to set up port-forwarding so your Prometheus instance can be accessible outside of your cluster.
But, before that, you should create the service monitor resource so that Prometheus can scrape metrics exposed by the locust-exporter.

```bash
k -n monitoring apply -f ./kubernetes-manifests/metrics/locust-servicemonitor.yaml

kubectl get svc -n monitoring

# wait some mininutes
kubectl port-forward svc/prometheus-kube-prometheus-prometheus -n monitoring 9090
```

Now, you can import the Grafana dashboard that show the application status.

```bash
# Admin Password
k -n monitoring get secret prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

# Admin User
k -n monitoring get secret prometheus-grafana -o jsonpath="{.data.admin-user}" | base64 --decode ; echo

kubectl port-forward svc/prometheus-grafana -n monitoring 8080:80

xclip -sel clip < ./kubernetes-manifests/grafana-dashboard.json

# Import the json dashboard ./kubernetes-manifests/grafana-dashboard.json
```

### Deploying the Kubernetes Metrics Server on a Cluster Using Kubectl

You can deploy the Kubernetes Metrics Server on clusters you created using Container Engine.

To deploy the Kubernetes Metrics Server on a cluster you've created with Container Engine for Kubernetes:

1. In a terminal window, deploy the Kubernetes Metrics Server by entering:

```bash
kubectl apply -f ./kubernetes-manifests/metrics/ms-components.yaml
```

2. Confirm that the Kubernetes Metrics Server has been deployed successfully and is available by entering:

```bash
kubectl get deployment metrics-server -n kube-system
```

### HPA - Horizontal Pod Autoscaling

Now, you can create the horizontal pod autoscaling resources.

```bash
k -n online-boutique apply -f ./kubernetes-manifests/hpa/hpa-manifest-cpu.yaml
```

## Test 2

### Creation of the Cluster

Before starting the test, you should create the cluster where you'll operate.

```bash
# Test 2
sudo kind create cluster --name cluster2 --kubeconfig $HOME/.kube/configC2 --image kindest/node:v1.23.5
sudo chmod 644 $HOME/.kube/configC2
echo "alias lc2=\"export KUBECONFIG=$HOME/.kube/configC2\"" >> $HOME/.bashrc

sudo kind create cluster --name cluster3 --kubeconfig $HOME/.kube/configC3 --image kindest/node:v1.23.5
sudo chmod 644 $HOME/.kube/configC3
echo "alias lc3=\"export KUBECONFIG=$HOME/.kube/configC3\"" >> $HOME/.bashrc

source $HOME/.bashrc
lc2
```

### Liqo installation

```bash
chmod +x ./scripts/liqoInstaller.sh
./scripts/liqoInstaller.sh
source <(liqoctl completion bash) >> $HOME/.bashrc

liqoctl install kind --cluster-name cluster2
lc3
liqoctl install kind --cluster-name cluster3
lc2
```

Using kubectl, you can also manually obtain the list of discovered foreign clusters:

```bash
kubectl get foreignclusters
```

If the peering has succeeded, you should see a virtual node (named liqo-*) in addition to your physical nodes:

```bash
kubectl get nodes
```

### Deploy of the application

```bash
k create ns online-boutique
kubectl label namespace online-boutique liqo.io/enabled=true
k apply -f ./kubernetes-manifests/online-boutique/boutique-manifests-affinity.yaml -n online-boutique
```

Once the demo application manifest is applied, you can observe the creation of the different pods. On the node column you can see if the pods are hosted by the local or remote cluster:

```bash
k get pods -n online-boutique -o wide
```

When all pods are running you can start the loadgenerator:

```bash
kubectl port-forward -n online-boutique service/loadgenerator 8089
```

I'm using 200 users with 1 second of spawn rate for my test.

Now, you can check that losut-exporter is monitoring the loadgenerator resource.

```bash
kubectl port-forward -n online-boutique service/locust-exporter 9646
```

### Prometheus and Locust exporter

Now, you can deploy the kube-prometheus stack Helm chart.

```bash
kubectl create namespace monitoring

# Add prometheus-community repo and update
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts && helm repo update

# Install
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring
```

Finally, run the following command to confirm your kube-prometheus stack deployment.

```bash
kubectl get pods -n monitoring
```

In order to scrape metrics exposed by the locust-exporter you should create the service monitor resource.

```bash
k -n monitoring apply -f ./kubernetes-manifests/metrics/locust-servicemonitor.yaml
```

You can see the metrics by importing the Grafana dashboard.

```bash
# Admin Password
k -n monitoring get secret prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

# Admin User
k -n monitoring get secret prometheus-grafana -o jsonpath="{.data.admin-user}" | base64 --decode ; echo

kubectl port-forward svc/prometheus-grafana -n monitoring 8080:80

xclip -sel clip < ./kubernetes-manifests/grafana-dashboard.json

# Import the json dashboard ./kubernetes-manifests/grafana-dashboard.json
```

### Deploying the Kubernetes Metrics Server on a Cluster Using Kubectl

You can deploy the Kubernetes Metrics Server on the cluster you created with the following commands:

```bash
kubectl apply -f ./kubernetes-manifests/metrics/ms-components.yaml
```

Confirm that the Kubernetes Metrics Server has been deployed successfully and is available by entering:

```bash
kubectl get deployment metrics-server -n kube-system
```

### HPA - Horizontal Pod Autoscaling

Now, you can create the horizontal pod autoscaling resources.

```bash
k -n online-boutique apply -f ./kubernetes-manifests/hpa/hpa-manifest-cpu.yaml
```

## Test 3

### Creation of the Cluster

Before starting the test, you should create the cluster where you'll operate.

```bash
# Test 3
sudo kind create cluster --name cluster4 --kubeconfig $HOME/.kube/configC4 --config ./kubernetes-manifests/kind/kind-manifestC4.yaml
sudo chmod 644 $HOME/.kube/configC4
echo "alias lc4=\"export KUBECONFIG=$HOME/.kube/configC4\"" >> $HOME/.bashrc

sudo kind create cluster --name cluster5 --kubeconfig $HOME/.kube/configC5 --config ./kubernetes-manifests/kind/kind-manifestC5.yaml
sudo chmod 644 $HOME/.kube/configC5
echo "alias lc5=\"export KUBECONFIG=$HOME/.kube/configC5\"" >> $HOME/.bashrc

source $HOME/.bashrc
lc4
```

### Liqo installation

```bash
chmod +x ./scripts/liqoInstaller.sh
./scripts/liqoInstaller.sh
source <(liqoctl completion bash) >> $HOME/.bashrc

NODE1=$(sudo docker ps | grep cluster4 | head -n1 | cut -d " " -f1)
sudo docker exec -it $NODE1 iptables -t nat -I KIND-MASQ-AGENT 2 --dst 10.20.0.0/16 -j RETURN
NODE2=$(sudo docker ps | grep cluster4 | tail -n1 | cut -d " " -f1)
sudo docker exec -it $NODE2 iptables -t nat -I KIND-MASQ-AGENT 2 --dst 10.20.0.0/16 -j RETURN

NODE1=$(sudo docker ps | grep cluster5 | head -n1 | cut -d " " -f1)
sudo docker exec -it $NODE1 iptables -t nat -I KIND-MASQ-AGENT 2 --dst 10.10.0.0/16 -j RETURN
NODE2=$(sudo docker ps | grep cluster5 | tail -n1 | cut -d " " -f1)
sudo docker exec -it $NODE2 iptables -t nat -I KIND-MASQ-AGENT 2 --dst 10.10.0.0/16 -j RETURN

lc4
liqoctl install kind --cluster-name cluster4 --version=416839b0915a8a0a7d78331b5efb76bde5444910

lc5
liqoctl install kind --cluster-name cluster5 --version=416839b0915a8a0a7d78331b5efb76bde5444910
```

Using kubectl, you can also manually obtain the list of discovered foreign clusters:

```bash
kubectl get foreignclusters
```

If the peering has succeeded, you should see a virtual node (named liqo-*) in addition to your physical nodes:

```bash
kubectl get nodes
```

### Linkerd installation

If this is your first time running Linkerd, you will need to download the linkerd CLI onto your local machine. The CLI will allow you to interact with your Linkerd deployment.

To install the CLI manually, run:

```bash
curl --proto '=https' --tlsv1.2 -sSfL https://run.linkerd.io/install | sh
export PATH=$PATH:$HOME/.linkerd2/bin

linkerd check --pre

lc4
linkerd install | kubectl apply -f -
linkerd check

liqoctl offload namespace linkerd --pod-offloading-strategy=Local --namespace-mapping-strategy=EnforceSameName
```

### Deploy of the application

```bash
kubectl create ns online-boutique

liqoctl offload namespace online-boutique --namespace-mapping-strategy=EnforceSameName

cat ./kubernetes-manifests/online-boutique/boutique-manifests-affinity.yaml | linkerd inject - | kubectl -n online-boutique apply -f -

linkerd -n online-boutique check --proxy
```

Once the demo application manifest is applied, you can observe the creation of the different pods. On the node column you can see if the pods are hosted by the local or remote cluster:

```bash
k get pods -n online-boutique -o wide
```

When all pods are running you can start the loadgenerator:

```bash
kubectl port-forward -n online-boutique service/loadgenerator 8089
```

I'm using 200 users with 1 second of spawn rate for my test.

Now, you can check that losut-exporter is monitoring the loadgenerator resource.

```bash
kubectl port-forward -n online-boutique service/locust-exporter 9646
```

### Prometheus and Locust exporter

Now, you can deploy the kube-prometheus stack Helm chart.

```bash
kubectl create namespace monitoring

# Add prometheus-community repo and update
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts && helm repo update

# Install
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring
```

Finally, run the following command to confirm your kube-prometheus stack deployment.

```bash
kubectl get pods -n monitoring
```

In order to scrape metrics exposed by the locust-exporter you should create the service monitor resource.

```bash
k -n monitoring apply -f ./kubernetes-manifests/metrics/locust-servicemonitor.yaml
```

You can see the metrics by importing the Grafana dashboard.

```bash
# Admin Password
k -n monitoring get secret prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

# Admin User
k -n monitoring get secret prometheus-grafana -o jsonpath="{.data.admin-user}" | base64 --decode ; echo

kubectl port-forward svc/prometheus-grafana -n monitoring 8080:80

xclip -sel clip < ./kubernetes-manifests/grafana-dashboard.json

# Import the json dashboard ./kubernetes-manifests/grafana-dashboard.json
```

### Deploying the Kubernetes Metrics Server on a Cluster Using Kubectl

You can deploy the Kubernetes Metrics Server on the cluster you created with the following commands:

```bash
lc4
kubectl apply -f ./kubernetes-manifests/metrics/ms-components.yaml

lc5 
kubectl apply -f ./kubernetes-manifests/metrics/ms-components.yaml
```

Confirm that the Kubernetes Metrics Server has been deployed successfully and is available by entering:

```bash
kubectl get deployment metrics-server -n kube-system
```

### HPA - Horizontal Pod Autoscaling

Now, you can create the horizontal pod autoscaling resources.

```bash
k -n online-boutique apply -f ./kubernetes-manifests/hpa/hpa-manifest-cpu.yaml
```

## Test 4

### Creation of the Cluster

Before starting the test, you should create the cluster where you'll operate.

```bash
# Test 4
sudo kind create cluster --name cluster6 --kubeconfig $HOME/.kube/configC6
sudo chmod 644 $HOME/.kube/configC6
echo "alias lc6=\"export KUBECONFIG=$HOME/.kube/configC6\"" >> $HOME/.bashrc

sudo kind create cluster --name cluster7 --kubeconfig $HOME/.kube/configC7
sudo chmod 644 $HOME/.kube/configC7
echo "alias lc7=\"export KUBECONFIG=$HOME/.kube/configC7\"" >> $HOME/.bashrc

sudo cp ./kubernetes-manifests/linkerd/config-multicluster.yaml $HOME/.kube/config-multicluster
sudo chmod 644 $HOME/.kube/config-multicluster
echo "alias lmc=\"export KUBECONFIG=$HOME/.kube/config-multicluster\"" >> $HOME/.bashrc

# NOTE: Now, you must replace the values in `$HOME/.kube/config-multicluster` file with the correct values from the files: `$HOME/.kube/configC6` and `$HOME/.kube/configC7`

source $HOME/.bashrc

sudo kubectl config --kubeconfig=$HOME/.kube/config-multicluster rename-context kind-cluster6 west
sudo kubectl config --kubeconfig=$HOME/.kube/config-multicluster rename-context kind-cluster7 east

lmc
```

### Deploy of the MetalLB

To work Linkerd, in a multi-cluster scenario, a service of type LoadBalancer is required, but Kubernetes does not offer an implementation of network load balancers for bare-metal clusters. If you’re not running on a supported IaaS platform (GCP, AWS, Azure…), LoadBalancers will remain in the “pending” state indefinitely when created. MetalLB aims to redress this imbalance by offering a network load balancer implementation.

You can deploy the MetalLB in your cluster by running the following commands:

> NOTE: [Installing metallb using default manifests](https://kind.sigs.k8s.io/docs/user/loadbalancer/).

```bash
kubectl --context=west apply -f https://raw.githubusercontent.com/metallb/metallb/v0.12.1/manifests/namespace.yaml

kubectl --context=west apply -f https://raw.githubusercontent.com/metallb/metallb/v0.12.1/manifests/metallb.yaml
```

To complete layer2 configuration, we need to provide metallb a range of IP addresses it controls. We want this range to be on the docker kind network.

You can see the kind network rage with this command:

```bash
sudo docker network inspect -f '{{.IPAM.Config}}' kind
```

Now, you must create the ConfigMap resource containing the desired range:

```bash
k --context=west apply -f - <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  namespace: metallb-system
  name: config
data:
  config: |
    address-pools:
    - name: default
      protocol: layer2
      addresses:
      - 172.18.1.1-172.18.1.255 # Change with the correct range
EOF
```

You must repeat these steps for the east cluster:

```bash
kubectl --context=east apply -f https://raw.githubusercontent.com/metallb/metallb/v0.12.1/manifests/namespace.yaml

kubectl --context=east apply -f https://raw.githubusercontent.com/metallb/metallb/v0.12.1/manifests/metallb.yaml

k --context=east apply -f - <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  namespace: metallb-system
  name: config
data:
  config: |
    address-pools:
    - name: default
      protocol: layer2
      addresses:
      - 172.18.2.1-172.18.2.255 # Change with the correct range
EOF
```

Secondly, you can check the communication between the two clusters by deploying two Nginx services and performing a curl command for each side:

```bash
k --context=west apply -f https://raw.githubusercontent.com/inlets/inlets-operator/master/contrib/nginx-sample-deployment.yaml
kubectl --context=west expose deployment nginx-1 --port=80 --type=LoadBalancer

k --context=east apply -f https://raw.githubusercontent.com/inlets/inlets-operator/master/contrib/nginx-sample-deployment.yaml
kubectl --context=east expose deployment nginx-1 --port=80 --type=LoadBalancer

export NGINX_NAME=$(k --context=west get po -l app=nginx --no-headers -o custom-columns=:.metadata.name)
export NGINX_ADDR=$(k --context=east get svc -l app=nginx -o jsonpath={'.items[0].status.loadBalancer.ingress[0].ip'})
kubectl --context=west exec --stdin --tty $NGINX_NAME -- /bin/bash -c "apt-get update && apt install -y curl && curl ${NGINX_ADDR}"

export NGINX_NAME=$(k --context=east get po -l app=nginx --no-headers -o custom-columns=:.metadata.name)
export NGINX_ADDR=$(k --context=west get svc -l app=nginx -o jsonpath={'.items[0].status.loadBalancer.ingress[0].ip'})
kubectl --context=east exec --stdin --tty $NGINX_NAME -- /bin/bash -c "apt-get update && apt install -y curl && curl ${NGINX_ADDR}"
```

### Creation of the trust anchor

Linkerd requires a shared trust anchor to exist between the installations in all clusters that communicate with each other. This is used to encrypt the traffic between clusters and authorize requests that reach the gateway so that your cluster is not open to the public internet.

> NOTE: For more information see the [official documentation](https://linkerd.io/2.11/tasks/multicluster/).

```bash
mkdir trust && cd ./trust

# Root CA
step certificate create root.linkerd.cluster.local root.crt root.key --profile root-ca --no-password --insecure

# Issuer credentials
step certificate create identity.linkerd.cluster.local issuer.crt issuer.key --profile intermediate-ca --not-after 8760h --no-password --insecure --ca root.crt --ca-key root.key
```

### Linkerd installation

To install linkerd run:

```bash
curl --proto '=https' --tlsv1.2 -sSfL https://run.linkerd.io/install | sh
export PATH=$PATH:$HOME/.linkerd2/bin

# Linkerd
linkerd install \
  --identity-trust-anchors-file root.crt \
  --identity-issuer-certificate-file issuer.crt \
  --identity-issuer-key-file issuer.key \
  | tee \
    >(kubectl --context=west apply -f -) \
    >(kubectl --context=east apply -f -)
```

You can verify that everything has come up successfully with a check:

```bash
for ctx in west east; do
  echo "Checking cluster: ${ctx} ........."
  linkerd --context=${ctx} check || break
  echo "-------------"
done
```

To install the multicluster components on both west and east, you can run:

```bash
# Multi-Cluster components:
# - Gateway
# - Service Mirror
# - Service Account

for ctx in west east; do
  echo "Installing on cluster: ${ctx} ........."
  linkerd --context=${ctx} multicluster install | \
    kubectl --context=${ctx} apply -f - || break
  echo "-------------"
done
```

Make sure the gateway comes up successfully by running:

```bash
for ctx in west east; do
  echo "Checking gateway on cluster: ${ctx} ........."
  kubectl --context=${ctx} -n linkerd-multicluster \
    rollout status deploy/linkerd-gateway || break
  echo "-------------"
done
```

Double check that the load balancer was able to allocate a public IP address by running:

```bash
for ctx in west east; do
  printf "Checking cluster: ${ctx} ........."
  while [ "$(kubectl --context=${ctx} -n linkerd-multicluster get service -o 'custom-columns=:.status.loadBalancer.ingress[0].ip' --no-headers)" = "<none>" ]; do
      printf '.'
      sleep 1
  done
  printf "\n"
done
```

The next step is to link west to east. This will create a credentials secret, a Link resource, and a service-mirror controller. The credentials secret contains a kubeconfig which can be used to access the target (east) cluster’s Kubernetes API.

```bash
# Retrieve the API Server address for the east cluster
kubectl --context=east proxy --port=8080 &

export API_SERVER_ADDR=$(curl http://localhost:8080/api/ | jq '.serverAddressByClientCIDRs[0].serverAddress' | sed 's/\"//g')

kill -9 %%

# Perform the link
linkerd --context=east multicluster link --cluster-name east --api-server-address="https://${API_SERVER_ADDR}"| kubectl --context=west apply -f -

# Retrieve the API Server address for the west cluster
kubectl --context=west proxy --port=8080 &

export API_SERVER_ADDR=$(curl http://localhost:8080/api/ | jq '.serverAddressByClientCIDRs[0].serverAddress' | sed 's/\"//g')

kill -9 %%

# Perform the link
linkerd --context=west multicluster link --cluster-name west --api-server-address="https://${API_SERVER_ADDR}" | kubectl --context=east apply -f -

# Some check
linkerd --context=west multicluster check
linkerd --context=east multicluster check
# with linkerd viz install
# linkerd --context=west multicluster gateways
# linkerd --context=east multicluster gateways
```

### Deploy of the application

```bash
k --context=west create ns online-boutique
k --context=east create ns online-boutique

cat ./kubernetes-manifests/online-boutique/boutique-west-manifest.yaml | linkerd inject - | k --context=west -n online-boutique apply -f -

cat ./kubernetes-manifests/online-boutique/boutique-east-manifest.yaml | linkerd inject - | k --context=east -n online-boutique apply -f -

# Traffic Split
cat ./kubernetes-manifests/linkerd/trafficsplit-west.yaml | k --context=west -n online-boutique apply -f -

cat ./kubernetes-manifests/linkerd/trafficsplit-east.yaml | k --context=east -n online-boutique apply -f -
```

Once the demo application manifest is applied, you can observe the creation of the different pods.

```bash
k --context=west get pods -n online-boutique -o wide
```

When all pods are running you can start the loadgenerator:

```bash
kubectl --context=west port-forward -n online-boutique service/loadgenerator 8089
```

I'm using 200 users with 1 second of spawn rate for my test.

Now, you can check that losut-exporter is monitoring the loadgenerator resource.

```bash
kubectl --context=west port-forward -n online-boutique service/locust-exporter 9646
```

### Prometheus and Locust exporter

Now, you can deploy the kube-prometheus stack Helm chart.

```bash
kubectl --context=west create namespace monitoring

# Add prometheus-community repo and update
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts && helm repo update

# Install
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring
```

Finally, run the following command to confirm your kube-prometheus stack deployment.

```bash
kubectl --context=west get pods -n monitoring
```

In order to scrape metrics exposed by the locust-exporter you should create the service monitor resource.

```bash
k --context=west -n monitoring apply -f ./kubernetes-manifests/metrics/locust-servicemonitor.yaml
```

You can see the metrics by importing the Grafana dashboard.

```bash
# Admin Password
k --context=west -n monitoring get secret prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

# Admin User
k --context=west -n monitoring get secret prometheus-grafana -o jsonpath="{.data.admin-user}" | base64 --decode ; echo

kubectl --context=west port-forward svc/prometheus-grafana -n monitoring 8080:80

xclip -sel clip < ./kubernetes-manifests/grafana-dashboard.json

# Import the json dashboard ./kubernetes-manifests/grafana-dashboard.json
```

### Deploying the Kubernetes Metrics Server on a Cluster Using Kubectl

You can deploy the Kubernetes Metrics Server on the cluster you created with the following commands:

```bash
kubectl --context=west apply -f ./kubernetes-manifests/metrics/ms-components.yaml

kubectl --context=east apply -f ./kubernetes-manifests/metrics/ms-components.yaml
```

Confirm that the Kubernetes Metrics Server has been deployed successfully and is available by entering:

```bash
kubectl --context=west get deployment metrics-server -n kube-system
```

### HPA - Horizontal Pod Autoscaling

Now, you can create the horizontal pod autoscaling resources.

```bash
k --context=west -n online-boutique apply -f ./kubernetes-manifests/hpa/hpa-manifest-cpu.yaml
```
