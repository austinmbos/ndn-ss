# containerizing applications ( building images )
- Each dir has the materials to build a docker container
- They are seperated by dirs for easy copying programs and needed files
into the container when building
- Each dir should have a Dockerfile 
- Each dir should have the needed files

## Steps to set up ndn/nfd docker
- First: build the ndn-base container, This is needed for nfd
```
cd docker/ndn-base
docker build -t ndn-base .
```
- Second: build the NFD-base container 
```
cd docker/nfd-base
docker build -t nfd-base .
```
- If all went well, there should be a runnable nfd now

- A helper script is being build to help control the NFD docker
container





## Overview of containers here ( so far )
### ndn-base
- This is the ndn-cxx base ubuntu image

### nfd-base
- this is build on ndn-base docker image, just with NFD installed and ready to
  go.


## What container images need to be worked on
- NFD container
	- entry node
	- exit node

- Microservice containers
	- signature verification

