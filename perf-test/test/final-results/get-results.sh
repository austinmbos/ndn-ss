#!/usr/bin/env bash

# get the results from the directory


sudo cp -r /var/lib/docker/volumes/results/_data/ .
sudo chown $(whoami):$(whoami) *
cd _data
sudo chown $(whoami):$(whoami) *
cd ..
