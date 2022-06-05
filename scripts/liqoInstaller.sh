#!/bin/bash

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

ARCH=none
OS=none

install_liqoctl
