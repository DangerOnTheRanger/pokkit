#!/usr/bin/env bash
set -o pipefail -o noclobber -o errexit -o nounset -o xtrace
docker build . --tag pokkit-client
docker run --cap-add SYS_ADMIN --device /dev/fuse --security-opt apparmor:unconfined pokkit-client --rm-pokkit-client
