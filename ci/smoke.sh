#!/bin/bash
set -ex

HOSTNAME=$1

apt-get update
apt-get install -y \
    dnsutils \
    curl \
    ;

nslookup $HOSTNAME
curl https://$HOSTNAME/ | grep "a plaintext pastebin service"
