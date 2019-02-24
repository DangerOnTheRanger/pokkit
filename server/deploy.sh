#!/usr/bin/env sh

# sane shell environment
set -o noclobber -o errexit -o nounset -o xtrace
cd $(dirname $0)

# apply general config
gcloud container clusters get-credentials standard-cluster-1 --zone us-central1-a --project pokkit
kubectl apply -f kubernetes.yaml
kubectl config set-context $(kubectl config current-context) --namespace=pokkit

# compile the latest code
COMMIT_SHA=$(git rev-parse HEAD)
PROJECT_ID=pokkit
GCR_IMAGE=gcr.io/${PROJECT_ID}/pokkit-server:${COMMIT_SHA}

docker build \
       --tag ${GCR_IMAGE} \
       --cache-from ${GCR_IMAGE} \
       .

# deploy latest code
gcloud auth configure-docker
docker push ${GCR_IMAGE}
kubectl set image deployment/pokkit-server pokkit-server=gcr.io/pokkit/pokkit-server:${COMMIT_SHA}

# do a test
kubectl port-forward $(kubectl get pods -l app=redis -o name) 6379 &
kubectl_proxy_pid=$!
sleep 2
redis-cli ping
kill $!
