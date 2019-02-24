#!/usr/bin/env bash

# sane shell environment
set -o pipefail -o noclobber -o errexit -o nounset -o xtrace
cd $(dirname $0)

COMMIT_SHA=$(git rev-parse HEAD)
PROJECT_ID=pokkit
GCR_IMAGE=gcr.io/${PROJECT_ID}/pokkit-client:${COMMIT_SHA}

# build
docker build \
       --tag ${GCR_IMAGE} \
       --cache-from ${GCR_IMAGE} \
       .

# test
docker run \
       --cap-add SYS_ADMIN \
       --device /dev/fuse \
       --security-opt apparmor:unconfined \
       --rm \
       ${GCR_IMAGE}

# auth and push (makes next build faster)
gcloud auth configure-docker
docker push ${GCR_IMAGE}
