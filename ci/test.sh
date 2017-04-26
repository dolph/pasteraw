#!/bin/bash
set -ex

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/../

# Install dependencies.
go get google.golang.org/appengine

# Run test suite.
go test
