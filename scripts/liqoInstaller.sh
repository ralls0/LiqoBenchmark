#!/bin/bash

function helper(){
  echo -e "This is a simple installer for liqoctl\n"
  echo "Usage:"
  echo -e "./liqoInstaller.sh [flags]\n"
  echo "Flags:"
  echo -e "  -cn,\t--cluster-name\t\t\tName of the cluster"
  echo -e "  -cc,\t--command-completition\t\tInject liqoctl completion into the configuretion file"
  echo -e "  -cp,\t--cluster-provider\t\tExport the KUBECONFIG file and install liqo into the cluster"
  echo ""
 
}

function install_liqoctl(){
  echo "[i] Looking for the architecture"
  ARCH=$(uname -m)
  case $ARCH in
    armv5*) ARCH="armv5";;
    armv6*) ARCH="armv6";;
    armv7*) ARCH="arm";;
    aarch64) ARCH="arm64";;
    arm64) ARCH="arm64";;
    x86) ARCH="386";;
    x86_64) ARCH="amd64";;
    i686) ARCH="386";;
    i386) ARCH="386";;
    *) 
      echo "[e] Error architecture '${ARCH}' unknown"
      exit 1 
    ;;
  esac
  echo "[i] Looking for the OS"
  OS=$(uname |tr '[:upper:]' '[:lower:]')
  case "$OS" in
    # Minimalist GNU for Windows
    "mingw"*) OS='windows'; return ;;
  esac
  if ! command -v liqoctl &> /dev/null
  then
    echo "[i] Install the latest version of liqoctl for: ${OS}-${ARCH}"
    curl --fail -LSO "https://get.liqo.io/liqoctl-${OS}-${ARCH}" && \
    chmod +x "liqoctl-${OS}-${ARCH}" && \
    sudo mv "liqoctl-${OS}-${ARCH}" /usr/local/bin/liqoctl
  else
    echo "[i] Liqo already installed"
  fi
}

function check_helm(){
  if ! command -v helm &> /dev/null
  then
    echo "[e] MISSING REQUIREMENT: helm could not be found on your system. Please install helm to continue: https://helm.sh/docs/intro/install/"
    exit 1;
  fi
}

function check_kind(){
  if ! command -v kind &> /dev/null
  then
    echo "[e] MISSING REQUIREMENT: kind could not be found on your system. Please install kind to continue: https://kind.sigs.k8s.io/docs/user/quick-start"
    exit 1;
  fi
}

function check_docker(){
  if ! command -v docker &> /dev/null;
  then
	  echo "[e] MISSING REQUIREMENT: docker engine could not be found on your system. Please install docker engine to continue: https://docs.docker.com/get-docker/"
	  exit 1
  fi
}

function check_kubectl(){
  if ! command -v kubectl &> /dev/null;
  then
	  echo "[e] MISSING REQUIREMENT: kubectl could not be found on your system. Please install kubectl engine to continue: https://kubernetes.io/docs/tasks/tools/"
	  exit 1
  fi
}

function check_kubeadm(){
  if ! command -v kubeadm &> /dev/null;
  then
	  echo "[e] MISSING REQUIREMENT: kubeadm could not be found on your system. Please install kubectl engine to continue: https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/"
	  exit 1
  fi
}

if [[ $(($# & 1)) == 1 ]]; then
  helper
  exit 1
fi

ARCH=none
OS=none
CLUSTER_NAME=liqoCluster
CLUSTER_PROVIDER=none

install_liqoctl
check_helm
check_docker
check_kubectl

i=1

while [[ i -lt $# ]]; do
  FLAG="$(cut -d ' ' -f $i <<< $@)"
  i=$((i+1))
  FVALUE="$(cut -d ' ' -f $i <<< $@)" 
  i=$((i+1))
  echo -e "[i] Parse ${FLAG} ${FVALUE}"
  case $FLAG in
    "-cn" | "--cluster-name")
      CLUSTER_NAME=$FVALUE
      echo -e "[i] Cluster name set to '${CLUSTER_NAME}'"
    ;;
    "-cc" | "--ccompletition")
      echo -e "[i] Load completions for each session"
      case $FVALUE in
        bash | BASH)
          source <(liqoctl completion bash) >> $HOME/.bashrc
        ;; 
        zsh | ZSH)
          liqoctl completion zsh > "${fpath[1]}/_liqoctl"
          source $HOME/.zshrc
        ;;
        fish | FISH)
          liqoctl completion fish > $HOME/.config/fish/completions/liqoctl.fish
	;;
        pshell | powershell | POWERSHELL)
          liqoctl completion powershell > liqoctl.ps1
        ;;
        *) 
          echo -e "[e] Error shell '${FVALUE}' unknown"
          exit 1
        ;;
      esac
    ;;
    "-cp" | "--cluster-provider")
      case $FVALUE in
        kind | KIND)
          check_kind
          echo "[q] Do you want to create a new cluster? [y/n]"
          read create;
          if [[ "${create}" -eq "y" ]]
          then 
            echo "[i] Cleaning: Deleting old clusters"
            kind delete cluster --name $CLUSTER_NAME
            if [ ! -d "$HOME/.kube" ]; then
              mkdir $HOME/.kube
            fi
            echo "[i] Creating cluster $CLUSTER_NAME"
            sudo kind create cluster --name $CLUSTER_NAME --kubeconfig $HOME/.kube/liqo_${CLUSTER_NAME}_config
            echo "alias liqo_${CLUSTER_NAME}_config=\"sudo export KUBECONFIG=$HOME/.kube/liqo_${CLUSTER_NAME}_config\"" >> $HOME/.zshrc
            echo -e "[i] If you want to select $CLUSTER_NAME, you should simply type:\nsource \$HOME/.zshrc # once\nliqo_${CLUSTER_NAME}_config"
            echo "[i] Exporting KUBECONFIG"
            export KUBECONFIG=$HOME/.kube/liqo_${CLUSTER_NAME}_config
            echo "[i] Install liqo into the for the $CLUSTER_NAME cluster"
            liqoctl install kind -n $CLUSTER_NAME
          else
            echo "[i] Retrieve configuration for the $CLUSTER_NAME cluster"
            kind get kubeconfig --name ${CLUSTER_NAME} > kind_kubeconfig
            echo "[i] Export kind_kubeconfig for the $CLUSTER_NAME cluster"
            export KUBECONFIG=kind_kubeconfig
            echo "[i] Install liqo into the for the $CLUSTER_NAME cluster"
            liqoctl install kind
          fi
        ;;
        k8s | K8s | K8S)
        check_kubeadm
        check_kubectl
        KCPATH="${HOME}/.kube/config"
        echo "[q] Is ${HOME}/.kube/config the KUBECONFIG path? [y/n]"
        read answ
        if [[ "$answ" -eq "n" ]]; then
          echo "[q] Insert the path: "
          read KCPATH
        fi
        echo "[i] Exporting KUBECONFIG"
        export KUBECONFIG=$KCPATH
        echo "[i] Install liqo into the cluster"
        liqoctl install kubeadm
        ;;
        *)
          helper
          exit 1;
        ;;
      esac
    ;;
    *)
      helper
      exit 1;
    ;;
    esac
done
