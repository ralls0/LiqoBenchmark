# Comandi utilizzati

```bash


```

## Addons

```bash
# Install
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release
```

## Docker

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

## Kind & kubectl

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

## Helm

```bash
# Check
command -v helm

# Install
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```

## Creazione clusters

```bash
sudo kind create cluster --name cluster1 --kubeconfig $HOME/.kube/configC1
sudo chmod 644 $HOME/.kube/configC1
echo "alias lc1=\"export KUBECONFIG=$HOME/.kube/configC1\"" >> $HOME/.bashrc
sudo kind create cluster --name cluster2 --kubeconfig $HOME/.kube/configC2
sudo chmod 644 $HOME/.kube/configC2
echo "alias lc2=\"export KUBECONFIG=$HOME/.kube/configC2\"" >> $HOME/.bashrc
sudo kind create cluster --name cluster3 --kubeconfig $HOME/.kube/configC3
sudo chmod 644 $HOME/.kube/configC3
echo "alias lc3=\"export KUBECONFIG=$HOME/.kube/configC3\"" >> $HOME/.bashrc
source $HOME/.bashrc
```

```bash
sudo kind create cluster --name cluster4 --kubeconfig $HOME/.kube/configC4
sudo chmod 644 $HOME/.kube/configC4
echo "alias lc4=\"export KUBECONFIG=$HOME/.kube/configC4\"" >> $HOME/.bashrc
sudo kind create cluster --name cluster5 --kubeconfig $HOME/.kube/configC5
sudo chmod 644 $HOME/.kube/configC5
echo "alias lc5=\"export KUBECONFIG=$HOME/.kube/configC5\"" >> $HOME/.bashrc
sudo kind create cluster --name cluster6 --kubeconfig $HOME/.kube/configC6
sudo chmod 644 $HOME/.kube/configC6
echo "alias lc6=\"export KUBECONFIG=$HOME/.kube/configC6\"" >> $HOME/.bashrc
source $HOME/.bashrc
```

## Clone Linkerd

```bash
git clone https://github.com/Ralls0/linkerd2.git
cd linkerd2
git checkout ral/liqo-ipam
sudo apt install -y jq
cd bin
./fetch-proxy
```

## Test 1

```bash
lc1
k create ns online-boutique
k apply -f https://raw.githubusercontent.com/Ralls0/LiqoBenchmark/main/kubernetes-manifests/ms-components.yaml
k apply -f https://raw.githubusercontent.com/Ralls0/LiqoBenchmark/ral/setup/kubernetes-manifests/kubernetes-manifests.yaml -n online-boutique
k apply -f https://raw.githubusercontent.com/Ralls0/LiqoBenchmark/main/kubernetes-manifests/hpa-manifest.yaml
```

## Test 2

```bash
curl -fsSL https://raw.githubusercontent.com/Ralls0/LiqoBenchmark/main/scripts/liqoInstaller.sh > liqoInstaller
chmod +x ./liqoInstaller
./liqoInstaller
source <(liqoctl completion bash) >> $HOME/.bashrc
lc2
liqoctl install kind --cluster-name cluster2
lc3
liqoctl install kind --cluster-name cluster3

```
