#!/bin/gnuplot -c

# Plot memory and CPU usage over time. Usage:

#  usage-plot.gp <input file> [<output .png file>]

# where the input file has the columns `<unix time> <memory, with m/g suffix> <% cpu>`

# To create the input file, see https://gist.github.com/jakubholynet/931a3441982c833f5f8fcdcf54d05c91

quit

# Arguments:

infile=ARG1
outfile=ARG2
set term x11
set title 'Memory, CPU usage from' . infile
set xdata time
set timefmt "%s"
set xlabel "Time [[hh:]mm:ss]"
set ylabel "Memory usage"
set format y '%.1s%cB'
set y2label 'CPU usage'
set format y2 '%.0s%%'
set y2tics nomirror
set tics out
set autoscale y
set autoscale y2

resolveUnit(u,mul,x)=(pos=strstrt(x,u), pos > 0 ? sprintf("%f",real(substr(x,1,pos - 1))*mul) : x)

resolveUnits(x)=(resolveUnit("g",1024*1024*1024,resolveUnit("m",1024*1024,x)))

check(x)=(real(resolveUnits(x)))

if (exists("outfile") && strlen(outfile) > 0) {
    print "Outputting to the file ", outfile
    set term png # 640,480
    set output outfile
}

# Styling
set style line 1 linewidth 2 linecolor 'blue'
set style line 2 linecolor 'light-green'

#set xtics font ", 10"
set tics font ", 10"
set xtics rotate 60 

plot infile u 1:3 with lp axes x1y2 title "cpu" linestyle 2, \
    infile using 1:(check(stringcolumn(2))) with linespoints title "memory" linestyle 1
