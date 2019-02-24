#!/usr/bin/env bash
set -o pipefail -o noclobber -o errexit -o nounset -o xtrace
docker build . --tag pokkit-client
docker run --name pokkit-client --rm pokkit-client
