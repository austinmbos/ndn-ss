#!/usr/bin/env bash

nfd-start 2> /dev/null &

sleep 1

hostname -i

./p 
