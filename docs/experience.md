# Liqo benchmark

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

Before starting each test case, you should create the cluster where you'll operate. The following commands create all clusters for the four tests:

```bash
# Test 1
sudo kind create cluster --name cluster1 --kubeconfig $HOME/.kube/configC1 --image kindest/node:v1.23.5
sudo chmod 644 $HOME/.kube/configC1
echo "alias lc1=\"export KUBECONFIG=$HOME/.kube/configC1\"" >> $HOME/.bashrc

source $HOME/.bash

# Test 2
sudo kind create cluster --name cluster2 --kubeconfig $HOME/.kube/configC2 --image kindest/node:v1.23.5
sudo chmod 644 $HOME/.kube/configC2
echo "alias lc2=\"export KUBECONFIG=$HOME/.kube/configC2\"" >> $HOME/.bashrc

sudo kind create cluster --name cluster3 --kubeconfig $HOME/.kube/configC3 --image kindest/node:v1.23.5
sudo chmod 644 $HOME/.kube/configC3
echo "alias lc3=\"export KUBECONFIG=$HOME/.kube/configC3\"" >> $HOME/.bashrc

source $HOME/.bash

# Test 3
sudo kind create cluster --name cluster4 --kubeconfig $HOME/.kube/configC4 --config ./kubernetes-manifests/kind-manifestC4.yaml
sudo chmod 644 $HOME/.kube/configC4
echo "alias lc4=\"export KUBECONFIG=$HOME/.kube/configC4\"" >> $HOME/.bashrc

sudo kind create cluster --name cluster5 --kubeconfig $HOME/.kube/configC5 --config ./kubernetes-manifests/kind-manifestC5.yaml
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




### INSTALL LIQO

Before installing Liqo, you should set the right `kubeconfig` for your cluster properly. The Liqo installer leverages `kubectl`: by default `kubectl` refers to the default identity in `~/.kube/config` but you can override this configuration by exporting a `KUBECONFIG` variable.

To do so, I'm going to use a simpe script (`scripts/liqoInstaller.sh`) that creates a cluster by means of `kind` and install Liqo on it.

> NOTE: For the official docs see the upstream: [liqoctl](https://doc.liqo.io/installation/#liqoctl)

