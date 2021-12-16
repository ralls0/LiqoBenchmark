#!/bin/bash

function install_helm(){
  if ! command -v helm &> /dev/null
  then
    echo "[i] Installing helm..."
    curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
    chmod 700 get_helm.sh
    ./get_helm.sh
  fi
}

function install_docker(){
  if ! command -v docker &> /dev/null
  then
	  echo "[i] Installing docker..."
	  sudo apt update
    sudo apt install ca-certificates curl gnupg lsb-release
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt update
    sudo apt install docker-ce docker-ce-cli containerd.io
  fi
}

function install_kind(){
  if ! command -v kind &> /dev/null
  then
    echo "[i] Installing kind..."
    curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.11.1/kind-linux-amd64
    chmod +x ./kind
    sudo mv ./kind /usr/bin/kind
  fi
}

function install_K8s(){
  if ! command -v kubeadm &> /dev/null
  then
    echo "[i] Installing kubelet, kubeadm and kubectl..."
    sudo apt update
    sudo apt install -y apt-transport-https ca-certificates curl
    sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
    echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
    sudo apt update
    sudo apt install -y kubelet kubeadm kubectl
    sudo apt-mark hold kubelet kubeadm kubectl
  fi
}

function personal_setup(){
  echo "[i] Replacing vimrc file..."
  mkdir $HOME/.tmp
  echo "$(curl -fsSL https://raw.githubusercontent.com/Ralls0/dotfiles/main/.vimrc)" > $HOME/.vimrc
  if ! command -v zsh &> /dev/null
  then
    echo "[i] Installing zsh..."
    sudo apt install zsh
  fi
  if [[ ! -d "$HOME/.oh-my-zsh" ]]
  then
    echo "[i] Installing oh-my-zsh..."
    sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
  fi
  if [[ ! -d "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k" ]]
  then
    echo "[i] Installing powerlevel10k theme..."
    git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
  fi 
  if [[ ! -d "$ZSH_CUSTOM/plugins/zsh-autosuggestions" ]]
  then
    echo "[i] Adding zsh-autosuggestions plugin..."
    git clone https://github.com/zsh-users/zsh-autosuggestions.git $ZSH_CUSTOM/plugins/zsh-autosuggestions
  fi 
  if [[ ! -d "$ZSH_CUSTOM/plugins/zsh-syntax-highlighting" ]]
  then  
    echo "[i] Adding zsh-syntax-highlighting plugin..."
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $ZSH_CUSTOM/plugins/zsh-syntax-highlighting
  fi 
  echo "[i] Replacing zshrc file..."
  echo "$(curl -fsSL https://raw.githubusercontent.com/Ralls0/dotfiles/main/.zshrc)" > $HOME/.zshrc
  source $HOME/.zshrc
}

install_docker
install_helm

echo "Would you like to use kind or K8s? [kind/k8s]"
read env
case $env in
  kind | Kind | KIND)
    install_kind
  ;;
  k8s | K8s | K8S)
    install_K8s
  ;;
  *)
    echo "[e] Error $env environment unknown"
    exit 1
  ;;
esac

echo "Would you like to add the personal setup? [y/n]"
read psetup
if [[ "$psetup" -eq "y" || "$psetup" -eq "Y" || "$psetup" -eq "yes" ]]
then
  personal_setup
fi
