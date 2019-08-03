#!/usr/bin/env bash

if [ "$1" = "--stop" ]; then
	echo "Stopping and quitting"
	docker container kill nfd_entry
	docker container kill sig_ver
	docker container kill sym_dec
	exit
fi

#########################################
# Run client for good and bad
#########################################


#docker run --name nfd_entry -d -v shared:/app/shared nfd-entry
#docker run --name sig_ver -d -v shared:/app/shared sig-ver
#docker run --name sym_dec -d -v shared:/app/shared sym_dec

docker start nfd_entry
docker start sig_ver
docker start sym_dec

sleep 3

for i in {1..2}; do
	echo "======= Good ======="
	python3 client-app.py good
	sleep 1
done

# start and stop to get a zero segment in the data output
docker container kill nfd_entry
docker container kill sig_ver
docker container kill sym_dec

echo "[*] Done with good tests, moving on to bad"
sleep 5

docker start nfd_entry
docker start sig_ver
docker start sym_dec


for i in {1..2}; do
	echo "======= Bad ======="
	python3 client-app.py bad
	sleep 1
done

docker container kill nfd_entry
docker container kill sig_ver
docker container kill sym_dec

