#!/usr/bin/env bash
set -o pipefail -o noclobber -o errexit -o nounset -o xtrace
COMMIT_SHA=$(git rev-parse HEAD)
PROJECT_ID=pokkit
IMAGE=gcr.io/${PROJECT_ID}/pokkit-client:${COMMIT_SHA}
docker run \
       --cap-add SYS_ADMIN \
       --device /dev/fuse \
       --security-opt apparmor:unconfined \
       --rm \
       ${IMAGE}
