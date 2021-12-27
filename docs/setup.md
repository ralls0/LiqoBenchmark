# SETUP

## PROVISION THE PLAYGROUND

Before starting to run the demos you should have installed some software on your system.

For my tests, I’m going to setup two clusters on a virtual machine hosted on [CrownLabs](https://crownlabs.polito.it/). The VM have 8 CORE and 16 GB of RAM.

> NOTE: On the `scripts` directory, there is a setup script with all commands below used.

First things first, I'm going to install helm because the `liqoctl` uses it to configure and install the Liqo by means of `helm chart`.

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```

Secondly, I'm going to install [kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installing-with-a-package-manager) (Kubernetes IN Docker)

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.11.1/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/bin/kind
```

### INSTALL LIQO

Before installing Liqo, you should set the right `kubeconfig` for your cluster properly. The Liqo installer leverages `kubectl`: by default `kubectl` refers to the default identity in `~/.kube/config` but you can override this configuration by exporting a `KUBECONFIG` variable.

To do so, I'm going to use a simpe script (`scripts/liqoInstaller.sh`) that creates a cluster by means of `kind` and install Liqo on it.

> NOTE: For the official docs see the upstream: [liqoctl](https://doc.liqo.io/installation/#liqoctl)

