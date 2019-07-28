#!/usr/bin/env bash

nfd-start 2> /dev/null &

echo 1 > sig-ver.sem
echo 1 > sym-dec.sem
echo 1 > final.sem

sleep 1

hostname -i

./p 
