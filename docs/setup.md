# Setup

## PROVISION THE PLAYGROUND

Before starting to run the demos  you should have installed some software on your system.

For my tests, I’m going to setup two clusters on a virtual machine hosted on [CrownLabs](https://crownlabs.polito.it/). The VM have 8 CORE and 16 GB of RAM.

First things first, I'm going to install helm due to the liqoctl uses it to configure and install the Liqo chart.

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

### Personal setup

In my case, I'm installing the zsh shell with [oh-my-zsh](https://ohmyz.sh/#install) and the [powerlevel10k](https://github.com/romkatv/powerlevel10k) theme. In addition, I'm setting up some of my personal [dotfiles](https://github.com/Ralls0/dotfiles) for the tools vim and zsh.

```bash
sudo apt install zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
git clone https://github.com/zsh-users/zsh-autosuggestions.git $ZSH_CUSTOM/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $ZSH_CUSTOM/plugins/zsh-syntax-highlighting
echo "$(curl -fsSL https://raw.githubusercontent.com/Ralls0/dotfiles/main/.zshrc)" > $HOME/.zshrc
mkdir $HOME/.tmp
echo "$(curl -fsSL https://raw.githubusercontent.com/Ralls0/dotfiles/main/.vimrc)" > $HOME/.vimrc
```