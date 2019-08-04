"""
graph throughput of the consumer application

options:

"""


from scipy.interpolate import make_interp_spline, BSpline
import statistics as stat
import matplotlib.pyplot as plt
import pylab
import json
import numpy as np
import sys

if len(sys.argv) == 1:
    print("Need what to process ")
    quit()

if sys.argv[1] == "single":
    #in_file = "do"
    out_file = "single-sig-ver"

if sys.argv[1] == "double":
    #in_file = "docker.bad.json"
    out_file = "single-sig-ver"


fig,ax = plt.subplots()

# NEED CHANGE
ax.plot(sym_dec_x,sym_dec_y,label="Sym Dec")
ax.plot(sig_ver_x,sig_ver_y,label="Sig Ver")
ax.plot(AGG_x,AGG_y,label="AGG")

ax.legend(loc='upper left')

ax.set(xlabel="Time (seconds)",ylabel='CPU Usage %',title="Scenario: "+out_file.capitalize())

pylab.ylim([0,20])
ax.grid()
fig.savefig(out_file+".png")




