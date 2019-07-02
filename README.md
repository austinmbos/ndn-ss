# ndn-ss ( ndn micro services )

- Notes and questions at the bottom of README
- Questions and topics are kept in a google doc ( add link here ? )
- services will have an ndn container at the entry and exit running NFD
- communcation between containers will happen with traditional IP
- Each service/container has their own dir to keep things clean. Change into the
  service dir that is desired and read the README for more info



### side notes ( for me )

- Dockerhub can be used to store these images or images can be tar'ed and
  shared.
- Need communication between microservices. 
	- For prototyping thinking flask web servers and json


## Working on right now

- Building/Testing nfd containers
- Building first microservice ( signature verification )
- How to take initial interest, pass data through service chain and return back
  to the user

## Getting started

- Setting up entry/exit points for microservices ( NFD containers )
    - These are how ndn traffic goes into the microservies ( as of now )

- Install docker ( the easy way, NOTE: not the official docker way to install )
```
sudo apt install docker.io
```
- TODO: switch to the official docker way



## saving your docker image/microservice for re-use
- TODO: ( using dockerhub or just keeping images local )
- When images are created locally, they are there for re-use


## Orchestration of ndn microservices ( later step )
- TODO:
- ideas for tools to use for ochestration: 
	* docker swarm
	* kubernetes
	* might need custom since ndn?


## Notes/Questions for ndn docker application ( microservices )

1. How to make sure application runs in container?

2. How to register with NFD on host machine? ( if microservice is an ndn
   application )

- Additional notes on each container or service can be found in its
  corresponding dir under the docker/ dir

