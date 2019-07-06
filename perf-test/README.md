# TODO:
- Build a script in each dir to perform the tests
	- It should get the necessary data
	- Run on the host
	- remove a previous image ( if exists )
	- build the docker image
	- Run the docker test
	- Consilidate the results

# Performance testing of microservices on bare metal and docker containers

- In each dir is instructions to run the microservice on bare metal or to use
  the docker file to build an image so the program can be run in a docker
  container with the same data.

- crypto-base is the docker image to use for running crypto applications in
  python

## Docker volumes
- Create a docker volume, or seperate volumes for the tests
```
docker volume create {name}
```
- To see what volumes are there to use
```
docker volume ls
```
- Docker volumes live at: /var/lib/docker/volumes

## Notes for running comparison tests
- In each dir, the code can be ran right there in the dir
- To run in docker, just build the image from Docker file
- Then run the container, BUT: attach a volume to get the results
- This will run the container with a volume
```
docker run -d -v results:/app/results {docker-images}
```
- NOTE: if you run on host BEFORE building the docker image, all the files will
  be copied over to the docker image, and when run, all the results will be
  available under the used docker volume storage
- Because of the previous, make sure a .docker. is attached to the log filename

## List of microservices
- sign
- sig-ver
- sym-enc
- sym-dec


## What code is ready to run
- sign
- sym-enc

