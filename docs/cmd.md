# Comandi utilizzati

## Addons

```bash
# Install
sudo apt update
sudo apt install -y apt-transport-https  ca-certificates curl gnupg lsb-release jq
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
sudo kind create cluster --name cluster4 --kubeconfig $HOME/.kube/configC4 --config ./kind-manifestc4.yaml
sudo chmod 644 $HOME/.kube/configC4
echo "alias lc4=\"export KUBECONFIG=$HOME/.kube/configC4\"" >> $HOME/.bashrc
sudo kind create cluster --name cluster5 --kubeconfig $HOME/.kube/configC5 --config ./kind-manifestc5.yaml # uguale ma con ip diversi
sudo chmod 644 $HOME/.kube/configC5
echo "alias lc5=\"export KUBECONFIG=$HOME/.kube/configC5\"" >> $HOME/.bashrc

#########
sudo kind create cluster --name cluster6 --kubeconfig $HOME/.kube/configC6
sudo chmod 644 $HOME/.kube/configC6
echo "alias lc6=\"export KUBECONFIG=$HOME/.kube/configC6\"" >> $HOME/.bashrc
source $HOME/.bashrc
```

## Clone Linkerd (old)

```bash
git clone https://github.com/Ralls0/linkerd2.git
cd linkerd2
git checkout ral/liqo-ipam
```

## Test 1

```bash
lc1
k create ns online-boutique
k apply -f https://raw.githubusercontent.com/Ralls0/LiqoBenchmark/main/kubernetes-manifests/ms-components.yaml
k apply -f https://raw.githubusercontent.com/ralls0/LiqoBenchmark/main/kubernetes-manifests/kubernetes-manifests.yaml -n online-boutique
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
k apply -f https://raw.githubusercontent.com/ralls0/LiqoBenchmark/main/kubernetes-manifests/kubernetes-manifests.yaml -n online-boutique
```

## Test 3

```bash
curl -fsSL https://raw.githubusercontent.com/Ralls0/LiqoBenchmark/main/scripts/liqoInstaller.sh > liqoInstaller
chmod +x ./liqoInstaller
./liqoInstaller
source <(liqoctl completion bash) >> $HOME/.bashrc
sudo docker exec -it 91ba37fd1e3b bash
iptables -t nat -I KIND-MASQ-AGENT 2 --dst 10.20.0.0/16 -j RETURN
sudo docker exec -it a9e6f3769054 bash
iptables -t nat -I KIND-MASQ-AGENT 2 --dst 10.20.0.0/16 -j RETURN
sudo docker exec -it fc19a0d39c38 bash
iptables -t nat -I KIND-MASQ-AGENT 2 --dst 10.10.0.0/16 -j RETURN
sudo docker exec -it 51f9ef8f339b bash
iptables -t nat -I KIND-MASQ-AGENT 2 --dst 10.10.0.0/16 -j RETURN
lc4
liqoctl install kind --cluster-name cluster4 --version=c169957721e85290aa19e0fefce4b5961538d532 --repo-url=https://github.com/giorio94/liqo
lc5
liqoctl install kind --cluster-name cluster5 --version=c169957721e85290aa19e0fefce4b5961538d532 --repo-url=https://github.com/giorio94/liqo
curl --proto '=https' --tlsv1.2 -sSfL https://run.linkerd.io/install | sh
export PATH=$PATH:/home/crownlabs/.linkerd2/bin
linkerd check --pre
lc4
linkerd install | kubectl apply -f -
linkerd check
liqoctl offload namespace linkerd --pod-offloading-strategy=Local --namespace-mapping-strategy=EnforceSameName
kubectl create ns online-boutique
liqoctl offload namespace online-boutique --namespace-mapping-strategy=EnforceSameName
curl -fsSL https://raw.githubusercontent.com/ralls0/LiqoBenchmark/main/kubernetes-manifests/kubernetes-manifests.yaml | linkerd inject - | kubectl -n online-boutique apply -f -
linkerd -n online-boutique check --proxy
k port-forward -n online-boutique svc/frontend-external 8080:80 --address=0.0.0.0
# oppure senza il flag --address ma con le seguenti regole:
# sudo ufw allow 8080
# sudo sysctl net.ipv4.ip_forward=1 
# sudo iptables -t nat -A PREROUTING -p tcp --dport 8080 -j DNAT --to-destination 127.0.0.1:8080
linkerd viz install | kubectl apply -f -
linkerd check
linkerd viz dashboard &
# In caso non funzioni e si deve accedere alla dashboard da un'altra VM:
# 1. Bisognava modificare un args come indicato [qui](https://linkerd.io/2.11/tasks/exposing-dashboard/#tweaking-host-requirement)
# 2. Aprimao la prota 50750 e mandiamo il traffico sulla porta indicata:
# sudo ufw allow 50750
# sudo sysctl net.ipv4.ip_forward=1 
# sudo iptables -t nat -A PREROUTING -p tcp --dport 50750 -j DNAT --to-destination 127.0.0.1:50750
```

### Old steps

```bash
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
