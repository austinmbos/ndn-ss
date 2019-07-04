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

## List of microservices
- Sign
- Sig-Ver
- Sym-Enc
- Sym-Dec

