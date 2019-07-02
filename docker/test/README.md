# Test case / example using simple python flask application

- This is the test directory to demonstrate how to put the pieces together in
this dir to build a docker image from Dockerfile and files.

- Needed components
	- Dockerfile ( example given )
	- any associated files for the program (example files given )

- To build the image from dockerfile
```
docker build -t flask-app-test .
```

- To run the newly created image
```
docker run -d -p 5000:5000 flask-app-test
```
- Explaination of the commands for running
	- -d : detach
	- -p : bind a port ( bind a port on the host to a port on the inside of the
	  container

### Notes
- This could be used as a base for building simple microservice containers that
  may use flask for their communication ( prototyping at lease )


