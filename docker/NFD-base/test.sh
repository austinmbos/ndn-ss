#!/usr/bin/env bash

#############################################################
#
#  build and ndn base image
#  build on ubuntu 
#  contains: ( pun intented )
#    NFD
#    obviously all deps for NFD
#
#   Note:
#     nfd will be installed globally
#
#
#############################################################

# This script gets ran when the image is built -- so when ran
# with docker build -t

# this is used to initialize the environment/install everything

# this script should build/set up everything so when the container
# is ran, it can be ran detached and the designated application will be ran


echo "building NFD docker container image ( nfd-base )"



##################
# set some envs
##################
CONT_NAME="nfd-base"
WORKDIR="/ndn"

# this was run in ndn-base
#mkdir $WORKDIR

#####################################
#
# install some deps
#
#####################################

apt update
apt -y install build-essential pkg-config libboost-all-dev \
                     libsqlite3-dev libssl-dev libpcap-dev

git clone --recursive https://github.com/named-data/NFD $WORKDIR/NFD


cd $WORKDIR/NFD
./waf configure
./waf
./waf install

cp /usr/local/etc/ndn/nfd.conf.sample /usr/local/etc/ndn/nfd.conf

# NFD should be installed now


