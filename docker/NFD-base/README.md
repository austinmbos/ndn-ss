# NFD-base

- This is the base NFD container
- It is build upon NDN-base to keep things modular
- Copies over slightly modified versions of nfd-start & nfd-stop

## Using nfd in the container
- If you wish to send an ndn packet through the service chain NFD needs to be
  installed on the host.
- Now before ndn packets can be sent into the NFD entry point of the service
  chain, a face to the running docker container must be made.
- To do this, use nfd to create a face to the container
```
TODO: how to create face to the container
```
