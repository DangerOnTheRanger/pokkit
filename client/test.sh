#!/usr/bin/env bash
set -o pipefail -o noclobber -o errexit -o nounset -o xtrace
cd $(dirname $0)

gcloud auth configure-docker
COMMIT_SHA=$(git rev-parse HEAD)
PROJECT_ID=pokkit
GCR_IMAGE=gcr.io/${PROJECT_ID}/pokkit-client:${COMMIT_SHA}

docker build \
       --tag ${GCR_IMAGE} \
       --cache-from ${GCR_IMAGE} \
       .

docker run \
       --cap-add SYS_ADMIN \
       --device /dev/fuse \
       --security-opt apparmor:unconfined \
       --rm \
       ${GCR_IMAGE}

docker push ${GCR_IMAGE}
