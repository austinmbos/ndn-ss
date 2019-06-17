# ndn-ss ( ndn micro services )
- Documentation on how to get ndn applications to run as microservices.
- As things progress, their notes will be taken here, including commands
to make reproduction as easy as possible.
- Notes and questions at the bottom of README

### side notes ( for me )
- Dockerhub can be used to store these images.
- Things I need to figure out:
	- What structure should the app be:
	- A producer
	- Or different logic


## Getting started
- Install docker ( the easy way, NOTE: not the official docker way to install )
```
sudo apt install docker.io
```
- TODO: switch to the official docker way


## Steps to create an 'ndn-ubuntu' container ready to go for ndn applications
- Create a default base docker ubuntu image
- Run the necessary commands inside the container set up an ndn environment
```
TODO
```
- TODO: create a script to simply the commands run inside container on start


## Creating a docker image ( That holds your application/microservice )
- Using the previously created 'ndn-ubuntu' image
- Example Dockerfile for you application
- ??? Can the application be a producer with no NFD inside container ???
```
TODO
```

## Connecting application inside container to host NFD
- TODO, if possible


## saving your docker image/microservice for re-use
- TODO: ( using dockerhub or just keeping images local )

## Orchestration of ndn microservices ( later step )
- TODO:
- ideas for tools to use for ochestration: 
	* docker swarm
	* kubernetes
	* might need custom since ndn?


## Notes/Questions for ndn docker application ( microservices )

1. What base to use?
* need a base image with necessary deps
* an ubuntu image with everything already packaged

2. How to make sure application runs in container?

3. How to register with NFD on host machine?

4. Does the application inside the container necessarily have to be a producer?
