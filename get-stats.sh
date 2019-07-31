#!/bin/sh

# Usage: ./monitor-usage.sh <PID of the process>

# Output: top.dat with lines such as `1539689171 305m 2.0`, i.e. unix time - memory with m/g suffix - CPU load in %

# To plot the output, see https://gist.github.com/jakubholynet/931a3441982c833f5f8fcdcf54d05c91

export PID=$1

rm top.dat

while true; do
	top -p $PID -bn 1 | egrep '^[0-9]+' | awk -v now=$(date +%s) '{print \
	now,$6,$9}' >> top.dat
done
