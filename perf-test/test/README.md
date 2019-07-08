# tests for performance between bare metal and docker

- To build the docker image
```
docker build -t perf-test .
```

- Run with volume
	- To create volume
	```
	docker volume create {name}
	```
	- To attach volume when running
	```
	docker run -v {volume}:{attach-point}
	```


- What I run
```
docker run -v results:/app/results
```
