# ndn-ss ( ndn micro services )
- Documentation on how to get ndn applications to run as microservices.
- As things progress, their notes will be taken here, including commands
to make reproduction as easy as possible.


## Creating a docker image ( steps )
- Need base ubuntu image
- Run necessary commands in plain container to set up
a ndn container
- Use this ndn container to create a plain docker image
that can compile/run ndn application inside.
- How to run this ndn application inside the container?

## Connecting application inside container to host NFD
- TODO

## Orchestration of ndn microservices
- TODO
- ideas for tools to use for ochestration: 
* docker swarm
* kubernetes
* might need custom since ndn?






Notes/Questions for ndn docker application

1. What base to use?
* need a base image with necessary deps
* an ubuntu image with everything already packaged

2. How to make sure application runs in container

3. How to register with NFD on host machine
