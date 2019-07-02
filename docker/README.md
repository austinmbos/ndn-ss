# containerizing applications ( building images )
- Each dir has the materials to build a docker container
- They are seperated by dirs for easy copying programs and needed files
into the container when building
- Each dir should have a Dockerfile 
- Each dir should have the needed files
- __NOTE: Since this uses all latest from github
  there may be unforseen issues, such as broken code in NFD__

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


## Steps to building entry and exit points
- This is a nfd docker container
- Make sure nfd-base image is ready to go
- Now an image can be built using nfd-base as the base! This means an ndn
  application can now run inside of a docker container.
- Now anytime the application needs to be updated, it is a very quick build for
  docker as ndn and nfd do NOT need to be rebuilt.
- To build the entry and exit points, go into their directory and follow the
  instructions
- associated dirs are ms-entry and ms-exit




## Overview of containers here ( so far )
### ndn-base
- This is the ndn-cxx base ubuntu image

### nfd-base
- this is build on ndn-base docker image, just with NFD installed and ready to
  go.

### service-entry-nfd
- This is the NFD entry point into the service chain

### service-exit-nfd
- This is the NFD exit point for the service chain


## What container images need to be worked on
- NFD container
	- entry node
	- exit node

- Microservice containers
	- signature verification

