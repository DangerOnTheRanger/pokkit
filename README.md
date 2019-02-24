# pokkit
The artist's version control system

## Install help

### Client side
The client requires `FUSE` to operate; you can setup and install `FUSE` in Debian with:
	
	sudo apt-get install fuse
	sudo modprobe fuse

I personally like `pipenv`.

    cd pokkit/client
    pipenv --three
    pipenv install -e . # installs packages from setup.py

### Server side
You'll want a kubernetes cluster running. If you don't have one, consider [installing minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/). If you choose minikube, you'll also need VirtualBox or KVM (see [this](https://github.com/kubernetes/minikube/blob/master/docs/drivers.md#kvm2-driver)).
