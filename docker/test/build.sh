#!/usr/bin/env bash

# so I don't have to remember the commands

echo " --build-image"
echo " --run-image"


if [ "$1" = "--build-image" ]; then
	docker build -t flask-app:latest . 
elif [ "$1" = "--run-image" ]; then
	docker run -d -p 5000:5000 flask-app
	echo "Started on port 5000"
fi

