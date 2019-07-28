#!/usr/bin/env bash


echo "Starting NFD"
nfd-start &
sleep 1


echo "Creating faces"
nfdc face create udp://172.17.0.2:6363
nfdc route add /ndn-ss udp://172.17.0.2:6363
sleep 1


echo "starting containers"
docker run -d -v shared:/app/shared nfd-entry
docker run -d -v shared:/app/shared sig-ver
docker run -d -v shared:/app/shared sym-dec
sleep 1


echo "Going into watch containers"
watch docker container ls



