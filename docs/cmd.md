# Comandi utilizzati

## Addons

```bash
# Aumento la capacita del disco su crownlabs
sudo growpart /dev/vda 2
sudo growpart /dev/vda 5
sudo resize2fs /dev/vda5

# My personal setup
mkdir -p liqo && cd liqo && curl https://raw.githubusercontent.com/ralls0/Simple-script/master/bash/personal_bash_setup > ./bashsetup && chmod +x ./bashsetup
./bashsetup
./bashsetup
source $HOME/.zshrc

# Install
sudo apt update
sudo apt install -y apt-transport-https  ca-certificates curl gnupg lsb-release jq
# Goland
wget https://go.dev/dl/go1.18.linux-amd64.tar.gz
sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.18.linux-amd64.tar.gz
# Step
wget https://dl.step.sm/gh-release/cli/docs-cli-install/v0.19.0/step-cli_0.19.0_amd64.deb
sudo dpkg -i step-cli_0.19.0_amd64.deb
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

## Linkerd

```bash
# Check
command -v linkerd

# Install
curl --proto '=https' --tlsv1.2 -sSfL https://run.linkerd.io/install | sh
export PATH=$PATH:$HOME/.linkerd2/bin
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

sudo kind create cluster --name cluster6 --kubeconfig $HOME/.kube/configC6
sudo chmod 644 $HOME/.kube/configC6
echo "alias lc6=\"export KUBECONFIG=$HOME/.kube/configC6\"" >> $HOME/.bashrc

sudo kind create cluster --name cluster7 --kubeconfig $HOME/.kube/configC7
sudo chmod 644 $HOME/.kube/configC7
echo "alias lc7=\"export KUBECONFIG=$HOME/.kube/configC7\"" >> $HOME/.bashrc

sudo curl -fsSL -o $HOME/.kube/config-multicluster https://raw.githubusercontent.com/ralls0/LiqoBenchmark/main/kubernetes-manifests/config-multicluster.yaml
sudo chmod 644 $HOME/.kube/config-multicluster
echo "alias lmc=\"export KUBECONFIG=$HOME/.kube/config-multicluster\"" >> $HOME/.bashrc

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
k apply -f https://raw.githubusercontent.com/Ralls0/LiqoBenchmark/main/kubernetes-manifests/hpa/hpa-manifest-cpu.yaml
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

## Test 4

```bash
# Modificare il file config-multicluster con i valori presenti in $HOME/.kube/configC6 e $HOME/.kube/configC7
sudo vim $HOME/.kube/config-multicluster
sudo kubectl config --kubeconfig=$HOME/.kube/config-multicluster rename-context kind-cluster6 west
sudo kubectl config --kubeconfig=$HOME/.kube/config-multicluster rename-context kind-cluster7 east
# Creiamo il trust anchor in modo che linkerd si interfacci tra i due cluster
step certificate create root.linkerd.cluster.local root.crt root.key --profile root-ca --no-password --insecure
# Creiamo le issuer credentials
step certificate create identity.linkerd.cluster.local issuer.crt issuer.key --profile intermediate-ca --not-after 8760h --no-password --insecure --ca root.crt --ca-key root.key
# Installazione metallb
kubectl --context=west apply -f https://raw.githubusercontent.com/metallb/metallb/v0.12.1/manifests/namespace.yaml
kubectl --context=west apply -f https://raw.githubusercontent.com/metallb/metallb/v0.12.1/manifests/metallb.yaml
sudo docker network inspect -f '{{.IPAM.Config}}' kind
# Guardiamo il range di valori dati e lo inseriamo dopo
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
# Installazione metallb
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
# Controllo che i due cluster comunichino
k --context=west apply -f https://raw.githubusercontent.com/inlets/inlets-operator/master/contrib/nginx-sample-deployment.yaml
k --context=east apply -f https://raw.githubusercontent.com/inlets/inlets-operator/master/contrib/nginx-sample-deployment.yaml
kubectl --context=west expose deployment nginx-1 --port=80 --type=LoadBalancer
kubectl --context=east expose deployment nginx-1 --port=80 --type=LoadBalancer
export NGINX_NAME=$(k --context=west get po -l app=nginx --no-headers -o custom-columns=:.metadata.name)
export NGINX_ADDR=$(k --context=east get svc -l app=nginx -o jsonpath={'.items[0].status.loadBalancer.ingress[0].ip'})
kubectl --context=west exec --stdin --tty $NGINX_NAME -- /bin/bash -c "apt-get update && apt install -y curl && curl ${NGINX_ADDR}"
export NGINX_NAME=$(k --context=east get po -l app=nginx --no-headers -o custom-columns=:.metadata.name)
export NGINX_ADDR=$(k --context=west get svc -l app=nginx -o jsonpath={'.items[0].status.loadBalancer.ingress[0].ip'})
kubectl --context=east exec --stdin --tty $NGINX_NAME -- /bin/bash -c "apt-get update && apt install -y curl && curl ${NGINX_ADDR}"

# Installiamo linkerd nei due cluster
# Si potrebbe bloccare alla creazione delle risorse ma va tutto bene
linkerd install \
  --identity-trust-anchors-file root.crt \
  --identity-issuer-certificate-file issuer.crt \
  --identity-issuer-key-file issuer.key \
  | tee \
    >(kubectl --context=west apply -f -) \
    >(kubectl --context=east apply -f -)

# Installazione viz
for ctx in west east; do
  linkerd --context=${ctx} viz install | \
    kubectl --context=${ctx} apply -f - || break
done

# Installazione dei componenti multicluster: Gateway, Service Mirror Service Account
for ctx in west east; do
  echo "Installing on cluster: ${ctx} ........."
  linkerd --context=${ctx} multicluster install | \
    kubectl --context=${ctx} apply -f - || break
  echo "-------------"
done

# Controllo che il gateway funzioni:
for ctx in west east; do
  echo "Checking gateway on cluster: ${ctx} ........."
  kubectl --context=${ctx} -n linkerd-multicluster \
    rollout status deploy/linkerd-gateway || break
  echo "-------------"
done

for ctx in west east; do
  printf "Checking cluster: ${ctx} ........."
  while [ "$(kubectl --context=${ctx} -n linkerd-multicluster get service -o 'custom-columns=:.status.loadBalancer.ingress[0].ip' --no-headers)" = "<none>" ]; do
      printf '.'
      sleep 1
  done
  printf "\n"
done

kubectl --context=east proxy --port=8080 &
export API_SERVER_ADDR=$(curl http://localhost:8080/api/ | jq '.serverAddressByClientCIDRs[0].serverAddress' | sed 's/\"//g')
kill -9 %%
linkerd --context=east multicluster link --cluster-name east --api-server-address="https://${API_SERVER_ADDR}"| kubectl --context=west apply -f -

kubectl --context=west proxy --port=8080 &
export API_SERVER_ADDR=$(curl http://localhost:8080/api/ | jq '.serverAddressByClientCIDRs[0].serverAddress' | sed 's/\"//g')
kill -9 %%
linkerd --context=west multicluster link --cluster-name west --api-server-address="https://${API_SERVER_ADDR}" | kubectl --context=east apply -f -

# Controllo link multicluster
linkerd --context=west multicluster check
linkerd --context=east multicluster check
linkerd --context=west multicluster gateways
linkerd --context=east multicluster gateways

k --context=west create ns online-boutique
k --context=east create ns online-boutique
k --context=west label ns online-boutique linkerd.io/inject=enabled
k --context=east label ns online-boutique linkerd.io/inject=enabled
curl https://raw.githubusercontent.com/ralls0/LiqoBenchmark/main/kubernetes-manifests/online-boutique-west-manifest.yaml | linkerd inject - | k --context=west -n online-boutique apply -f -
curl https://raw.githubusercontent.com/ralls0/LiqoBenchmark/main/kubernetes-manifests/online-boutique-east-manifest.yaml | linkerd inject - | k --context=east -n online-boutique apply -f -

linkerd --context=west -n online-boutique viz stat --from deploy/frontend svc
linkerd --context=west viz dashboard 

curl https://raw.githubusercontent.com/ralls0/LiqoBenchmark/main/kubernetes-manifests/trafficsplit-west.yaml | k --context=west -n online-boutique apply -f -
curl https://raw.githubusercontent.com/ralls0/LiqoBenchmark/main/kubernetes-manifests/trafficsplit-east.yaml | k --context=east -n online-boutique apply -f -

linkerd --context=west -n online-boutique viz stat trafficsplit

```

## Unistall Linkerd

```bash
linkerd viz uninstall | tee \
    >(kubectl --context=west delete -f -) \
    >(kubectl --context=east delete -f -)

linkerd --context=west multicluster unlink --cluster-name=east | kubectl --context=west delete -f -
linkerd --context=east multicluster unlink --cluster-name=west | kubectl --context=east delete -f -

linkerd multicluster uninstall | tee \
    >(kubectl --context=west delete -f -) \
    >(kubectl --context=east delete -f -)


linkerd uninstall | tee \
    >(kubectl --context=west delete -f -) \
    >(kubectl --context=east delete -f -)
```

## Integrare Prometheus

```bash
k -n linkerd-viz edit cm prometheus-config
### LINKERD ###
- job_name: 'linkerd'
  kubernetes_sd_configs:
  - role: pod
    namespaces:
      names: ['linkerd-viz']

  relabel_configs:
  - source_labels:
    - __meta_kubernetes_pod_container_name
    action: keep
    regex: ^prometheus$

  honor_labels: true
  metrics_path: '/federate'

  params:
    'match[]':
      - '{job="linkerd-proxy"}'
      - '{job="linkerd-controller"}'

### LOCUST EXPORTER ###
- job_name: 'locust'
  scrape_interval: 5s
  static_configs:
  - targets:
    - locust-exporter.online-boutique:9646

k -n online-boutique apply -f - <<EOF
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: locust-exporter
  namespace: online-boutique
  labels:
    demo: monitoring
spec:
  selector:
    matchLabels:
      app: locust-exporter
  endpoints:
  - port: metrics
    interval: 10s
EOF


k --context=west -n online-boutique exec -c server -it $(k --context=west -n online-boutique get po -l app=frontend --no-headers -o custom-columns=:.metadata.name) -- /bin/sh -c "apk add curl && curl -G --data-urlencode 'match[]={job=\"linkerd-proxy\"}' --data-urlencode 'match[]={job=\"linkerd-controller\"}' http://prometheus.linkerd-viz.svc.cluster.local:9090/federate"

k --context=west -n online-boutique exec -c server -it $(k --context=west -n online-boutique get po -l app=frontend --no-headers -o custom-columns=:.metadata.name) -- /bin/sh -c "apk add curl && curl http://prometheus.linkerd-viz.svc.cluster.local:9090/api/v1/query?query=request_total"
```


## Prove Locust

```bash
# edit deploy e aggiunta porta
# Creazione service
k --context=west -n online-boutique exec -c server -it $(k --context=west -n online-boutique get po -l app=frontend --no-headers -o custom-columns=:.metadata.name) -- /bin/sh -c "curl -v loadgenerator:8089" # apk add curl &&

k --context=west -n online-boutique exec -c main -it $(k --context=west -n online-boutique get po -l app=loadgenerator --no-headers -o custom-columns=:.metadata.name) -- /bin/sh 
# apt update && apt install -y net-tools

k --context=west -n online-boutique exec -c server -it $(k --context=west -n online-boutique get po -l app=frontend --no-headers -o custom-columns=:.metadata.name) -- /bin/sh -c "apk add curl && curl -v loadgenerator:9646"
```

## Custom API Server

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm -n linkerd --namespace linkerd \
  install prometheus-adapter prometheus-community/prometheus-adapter \
  -f https://raw.githubusercontent.com/Ralls0/LiqoBenchmark/main/kubernetes-manifests/hpa/prometheus-adapter.yaml

kubectl get --raw /apis/custom.metrics.k8s.io/v1beta1 | jq .

kubectl get --raw "/apis/custom.metrics.k8s.io/v1beta1/namespaces/linkerd/pods/*/response_per_second" | jq .

kubectl get --raw "/apis/custom.metrics.k8s.io/v1beta1/namespaces/leaderboard/pods/*/response_latency_ms_99th" | jq .

linkerd -n online-boutique stat deploy/frontend

k -n online-boutique apply -f https://raw.githubusercontent.com/Ralls0/LiqoBenchmark/main/kubernetes-manifests/hpa/hpa-manifest-linkerd-latency.yaml
```
