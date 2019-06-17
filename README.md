# ndn-ss ( ndn micro services )
- Documentation on how to get ndn applications to run as microservices.
- As things progress, their notes will be taken here, including commands
to make reproduction as easy as possible.
- Notes and questions at the bottom of README


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

## Orchestration of ndn microservices ( later step )
- TODO
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
