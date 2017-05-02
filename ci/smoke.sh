#!/bin/bash
set -ex

HOSTNAME=$1

curl https://$HOSTNAME/ | grep "a plaintext pastebin service"
