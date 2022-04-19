# Comandi utilizzati

## Addons

```bash
# Install
sudo apt update
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release
wget https://go.dev/dl/go1.18.linux-amd64.tar.gz
sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.18.linux-amd64.tar.gz
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

> --config al posto di --image
> sudo kind create cluster --name cluster1 --kubeconfig $HOME/.kube/configC1 --config ./kind-manifest.yaml


> docker eseguire:
> docker exec -it <nomeContainer> bash
> iptables -t nat -I KIND-MASQ-AGENT 2 --dst 10.10.0.0/16 -j RETURN

> liqoctl offload namespace linkerd --pod-offloading-strategy=Local --namespace-mapping-strategy=EnforceSameName
> liqoctl offload namespace onlineboutique --namespace-mapping-strategy=EnforceSameName

```bash
sudo kind create cluster --name cluster1 --kubeconfig $HOME/.kube/configC1 --image kindest/node:v1.23.5
sudo chmod 644 $HOME/.kube/configC1
echo "alias lc1=\"export KUBECONFIG=$HOME/.kube/configC1\"" >> $HOME/.bashrc
sudo kind create cluster --name cluster2 --kubeconfig $HOME/.kube/configC2 --image kindest/node:v1.23.5
sudo chmod 644 $HOME/.kube/configC2
echo "alias lc2=\"export KUBECONFIG=$HOME/.kube/configC2\"" >> $HOME/.bashrc
sudo kind create cluster --name cluster3 --kubeconfig $HOME/.kube/configC3 --image kindest/node:v1.23.5
sudo chmod 644 $HOME/.kube/configC3
echo "alias lc3=\"export KUBECONFIG=$HOME/.kube/configC3\"" >> $HOME/.bashrc
source $HOME/.bashrc
```

```bash
sudo kind create cluster --name cluster4 --kubeconfig $HOME/.kube/configC4 --image kindest/node:v1.23.5
sudo chmod 644 $HOME/.kube/configC4
echo "alias lc4=\"export KUBECONFIG=$HOME/.kube/configC4\"" >> $HOME/.bashrc
sudo kind create cluster --name cluster5 --kubeconfig $HOME/.kube/configC5  --image kindest/node:v1.23.5
sudo chmod 644 $HOME/.kube/configC5
echo "alias lc5=\"export KUBECONFIG=$HOME/.kube/configC5\"" >> $HOME/.bashrc

#########
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
lc2
liqoctl generate-add-command
lc3
<output of liqoctl generate-add-command command>
lc2
k create ns online-boutique
kubectl label namespace online-boutique liqo.io/enabled=true 
k apply -f https://raw.githubusercontent.com/Ralls0/LiqoBenchmark/ral/setup/kubernetes-manifests/kubernetes-manifests.yaml -n online-boutique
```

## Test 3

```bash
curl -fsSL https://raw.githubusercontent.com/Ralls0/LiqoBenchmark/main/scripts/liqoInstaller.sh > liqoInstaller
chmod +x ./liqoInstaller
./liqoInstaller
source <(liqoctl completion bash) >> $HOME/.bashrc
lc4
# --chart-path=: il path del repo da cui prendere la versione
liqoctl install kind --cluster-name cluster4 --version=8986c385adca13b476c4541ac03a5a6ccf38808d --chart-path=liqo/liqo/deployments/liqo
lc5
liqoctl install kind --cluster-name cluster5 --version=8986c385adca13b476c4541ac03a5a6ccf38808d --chart-path=liqo/liqo/deployments/liqo
git clone https://github.com/Ralls0/linkerd2.git
cd linkerd2
git checkout ral/liqo-ipam
# https://github.com/linkerd/linkerd2/blob/main/BUILD.md
export PATH=$PWD/bin:$PATH
linkerd version --client
linkerd check --pre
# In caso di problemi di kubectl version
curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.22.0/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl $(which kubectl)
linkerd check --pre
###
linkerd install | kubectl apply -f -
linkerd check
# cambiare le image dei container da cr.l5d.io/linkerd a ghcr.io/ralls0/linkerd2
# aggiunto:
           initialDelaySeconds: 300
#          periodSeconds: 30
# dopo readinessProbe e livenessProbe

```