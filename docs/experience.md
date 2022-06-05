# Liqo benchmark

## Intro

Nowadays more and more enterprises use and orchestrate more than one cloud platform to deliver application services. In this context is born the Liqo project which enables the creation of a multi-cluster environment. Moreover, the Service Mesh is a new technology that is being developed. It provides features like observability, reliability, security, and even a better Load Balancing than Kubernetes ones. This project aims at simulating a real scenario where a micro-services application like Online Boutique provided by Google, which includes multiple cooperating services, wants to scale based on the workloads reached into the cluster and on more clusters. During the project, the candidate will work to design, setup, implement and compare different scenarios and service mesh solutions like Service Mesh on Liqo or Linkerd.

## Provision the playground

Before starting to run the demos you should have installed some software on your system.

For my tests, I’m going to setup the clusters on the virtual machines hosted on [CrownLabs](https://crownlabs.polito.it/). > VMs: 4 CORE, 8 GB of RAM, and 25 GB of disk.

> NOTE: By default, not all 25 GB are available. You can use these commands to extend the disk:

```bash
sudo growpart /dev/vda 2
sudo growpart /dev/vda 5
sudo resize2fs /dev/vda5
```

First things first, I'm going to install some extra tools, and all the necessary dependencies on all the VMs:

```bash
sudo apt update
sudo apt install -y apt-transport-https  ca-certificates curl gnupg lsb-release jq

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

### Linkerd

```bash
# Check
command -v linkerd

# Install
curl --proto '=https' --tlsv1.2 -sSfL https://run.linkerd.io/install | sh
export PATH=$PATH:$HOME/.linkerd2/bin
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

## Creation of the Clusters

```bash
# Test 2
sudo kind create cluster --name cluster2 --kubeconfig $HOME/.kube/configC2 --image kindest/node:v1.23.5
sudo chmod 644 $HOME/.kube/configC2
echo "alias lc2=\"export KUBECONFIG=$HOME/.kube/configC2\"" >> $HOME/.bashrc

sudo kind create cluster --name cluster3 --kubeconfig $HOME/.kube/configC3 --image kindest/node:v1.23.5
sudo chmod 644 $HOME/.kube/configC3
echo "alias lc3=\"export KUBECONFIG=$HOME/.kube/configC3\"" >> $HOME/.bashrc

source $HOME/.bash

# Test 3
sudo kind create cluster --name cluster4 --kubeconfig $HOME/.kube/configC4 --config ./kubernetes-manifests/kind/kind-manifestC4.yaml
sudo chmod 644 $HOME/.kube/configC4
echo "alias lc4=\"export KUBECONFIG=$HOME/.kube/configC4\"" >> $HOME/.bashrc

sudo kind create cluster --name cluster5 --kubeconfig $HOME/.kube/configC5 --config ./kubernetes-manifests/kind/kind-manifestC5.yaml
sudo chmod 644 $HOME/.kube/configC5
echo "alias lc5=\"export KUBECONFIG=$HOME/.kube/configC5\"" >> $HOME/.bashrc

source $HOME/.bash

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

### Prometheus and Locust exporter

Grafana and Prometheus Kubernetes Cluster monitoring provides information on potential performance bottlenecks, cluster health, performance metrics. At the same time, visualize network usage, resource usage patterns of pods, and a high-level overview of what is going on in your cluster.

But before setting up a monitoring system with Grafana and Prometheus, you’ll first deploy the kube-prometheus stack Helm chart. The stack contains Prometheus, Grafana, Alertmanager, Prometheus operator, and other monitoring resources.

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
kubectl get svc -n monitoring
```

You’ll use the Prometheus service to set up port-forwarding so your Prometheus instance can be accessible outside of your cluster.

```bash
kubectl port-forward svc/prometheus-kube-prometheus-prometheus -n monitoring 9090
```



### Deploying the Kubernetes Metrics Server on a Cluster Using Kubectl

You can deploy the Kubernetes Metrics Server on clusters you create using Container Engine.

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

```bash
k apply -f ./kubernetes-manifests/hpa/hpa-manifest-cpu.yaml
```

### INSTALL LIQO

To do so, I'm going to use a simpe script (`scripts/liqoInstaller.sh`) that creates a cluster by means of `kind` and install Liqo on it.

> NOTE: For the official docs see the upstream: [liqoctl](https://doc.liqo.io/installation/#liqoctl)

