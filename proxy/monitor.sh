#!/usr/bin/env bash

# script to run the helping of monitoring docker container cpu usage

if [ $# == 0 ]; then
	echo "./monitor.sh sig/sym good/bad"
	exit
fi

if [ "$1" = "sig" ]; then
	if [ "$2" = "good" ]; then
		docker stats --format " $(date +%M:%S) sig-ver-good {{.CPUPerc}}" \
			sig_ver | tee sig-good.txt
	elif [ "$2" = "bad" ]; then
		docker stats --format " $(date +%M:%S) sig-ver-bad {{.CPUPerc}}" \
			sig_ver | tee sig-bad.txt
	else
		echo "Need a valid option"
	fi
elif [ "$1" = "sym" ]; then
	if [ "$2" = "good" ]; then
		docker stats --format " $(date +%M:%S) sym-dec-good {{.CPUPerc}}" \
			sym_dec | tee sym-good.txt
	elif [ "$2" = "bad" ]; then
		docker stats --format " $(date +%M:%S) sym-dec-bad {{.CPUPerc}}" \
			sym_dec | tee sym-bad.txt
	else
		echo "Need a valid option"
	fi
fi
