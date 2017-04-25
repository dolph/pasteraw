#!/bin/bash
set -ex

PROJECT=$1
KEY=$2

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Authenticate with Google Cloud
echo "$KEY" | base64 --decode > key_file.json
gcloud auth activate-service-account \
    --key-file=key_file.json

# Configure SDK
gcloud config set project $PROJECT

# Deploy the application
gcloud app deploy --quiet $DIR/../app.yaml
