#!/usr/bin/env bash

if [ $# = 0 ]; then
	echo "Need options, good or bad test,, or clean"
	exit
fi

# DEFINES
NUM_TESTS=100
#echo "Running ' $NUM_TESTS ' times "


if [ "$1" = "--rebuild" ]; then
	echo "Rebuilding containers; make sure images are built, and all containers"
	echo "are stopped and removed/cleaned"

	docker run --name nfd_entry_single -d -v shared:/app/shared nfd-entry-single
	sleep 5
	docker container kill nfd_entry_single
	docker run --name nfd_entry -d -v shared:/app/shared nfd-entry
	
	docker run --name sig_ver_1 -d -v shared:/app/shared sig-ver-1
	docker run --name sig_ver_2 -d -v shared:/app/shared sig-ver-2
	docker run --name sym_dec   -d -v shared:/app/shared sym-dec
	exit

fi


if [ "$1" = "--clear-logs" ]; then
	if [[ -z $2 ]]; then
		echo "No container specified"
		exit 1
	fi
	if [[ "$(docker ps -aq -f name=^/${2}$ 2> /dev/null)" == "" ]]; then
		echo "Container \"$2\" does not exist, exiting."
		exit 1
	fi
	log=$(docker inspect -f '{{.LogPath}}' $2 2> /dev/null)
	sudo truncate -s 0 $log
	exit
fi
	

if [ "$1" = "--stop" ]; then
	echo "Stopping and quitting"
	docker container kill nfd_entry
	docker container kill nfd_entry_single
	docker container kill sig_ver_1
	docker container kill sig_ver_2
	docker container kill sym_dec
	exit
fi

if [ "$1" = "--start-single" ]; then
	echo "Starting containers"
	docker container start nfd_entry_single
	docker container start sig_ver_1
	docker container start sym_dec
	exit
fi

if [ "$1" = "--start-double" ]; then
	echo "Starting containers"
	docker container start nfd_entry
	docker container start sig_ver_1
	docker container start sig_ver_2
	docker container start sym_dec
	exit
fi


if [ "$1" = "--setup" ]; then
	echo "Creating face and route for nfd/docker"
	nfdc face create udp://172.17.0.2:6363
	sleep 0.5
	nfdc route add /ndn-ss udp://172.17.0.2:6363
	exit
fi



#docker run --name nfd_entry -d -v shared:/app/shared nfd-entry
#docker run --name sig_ver -d -v shared:/app/shared sig-ver
#docker run --name sym_dec -d -v shared:/app/shared sym_dec

docker start nfd_entry
docker start sig_ver
docker start sym_dec

# let them all start
sleep 3


###############################
# run the good tests
###############################
if [ "$1" = "good" ]; then
	for ((i = 0; i<$NUM_TESTS; i++)); do
		echo "======= Good ======="
		python3 client-app.py good
		sleep 0.2
	done
fi


###############################
# run the bad tests
###############################
if [ "$1" = "bad" ]; then
	for ((i = 0; i<$NUM_TESTS; i++)); do
		echo "======= Bad ======="
		python3 client-app.py bad
		sleep 0.2
	done
fi


# finished, stop the containers
docker container kill nfd_entry
docker container kill sig_ver
docker container kill sym_dec



