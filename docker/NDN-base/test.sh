#!/usr/bin/env bash

#############################################################
#
#  build and ndn base image
#  build on ubuntu 
#  contains: ( pun intented )
#    ndn-cxx
#    NFD
#    obviously all deps the previous two need
#
#   Note:
#     ndn will be installed globally
#
#
#############################################################

# This script gets ran when the image is built -- so when ran
# with docker build -t

# this is used to initialize the environment/install everything

# this script should build/set up everything so when the container
# is ran, it can be ran detached and the designated application will be ran


echo "building ndn docker container image ( ndn-base )"



##################
# set some envs
##################
CONT_NAME="ndn-base"
WORKDIR="/ndn"

mkdir $WORKDIR

#####################################
#
# install some deps
#
#####################################

apt update
apt install -y git python build-essential libboost-all-dev libssl-dev libsqlite3-dev pkg-config python-minimal


git clone https://github.com/named-data/ndn-cxx.git $WORKDIR/ndn-cxx

cd $WORKDIR/ndn-cxx
./waf configure
./waf
./waf install

ldconfig

# ndn-cxx should be installed now


#####################################
#
# now to install NFD
#
#####################################

