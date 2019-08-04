"""
process the data from dockercpu.dat
"""



from scipy.interpolate import make_interp_spline, BSpline
import statistics as stat
import matplotlib.pyplot as plt
import pylab
import json
import numpy as np
import sys

if len(sys.argv) <= 1:
    print("python3 gather.py docker.good.json honest")
    print("python3 gather.py docker.bad.json malicious")
    quit()

if sys.argv[1] == "good":
    in_file = "docker.good.json"
    out_file = "honest"

if sys.argv[1] == "bad":
    in_file = "docker.bad.json"
    out_file = "malicious"

factor = 120

with open(in_file,"r") as f:
    c = json.load(f)

a = c['sym_dec']['cpu_perc']
b = c['sig_ver']['cpu_perc']
avg = []

for x in range(0,len(a)):
    avg.append( (a[x]+b[x])/2 )




offset = len(c['sym_dec']['cpu_perc']) - len(c['sym_dec']['time'])

sym_dec_orig = np.array(c['sym_dec']['time'][0:offset])
sym_dec_y = np.array(c['sym_dec']['cpu_perc'])
sym_dec_x = np.linspace(sym_dec_orig.min(),sym_dec_orig.max(),factor)
spl = make_interp_spline(sym_dec_orig,sym_dec_y,k=3)
sym_dec_y = spl(sym_dec_x)

sig_ver_orig = np.array(c['sig_ver']['time'][0:offset])
sig_ver_y = np.array(c['sig_ver']['cpu_perc'])
sig_ver_x = np.linspace(sig_ver_orig.min(),sig_ver_orig.max(),factor)
spl = make_interp_spline(sig_ver_orig,sig_ver_y,k=3)
sig_ver_y = spl(sig_ver_x)

avg_orig = np.array(c['sig_ver']['time'][0:offset])
avg_y = np.array(avg)
avg_x = np.linspace(avg_orig.min(),avg_orig.max(),factor)
spl = make_interp_spline(avg_orig,avg_y,k=3)
avg_y = spl(avg_x)


nfd_entry_orig = np.array(c['nfd_entry']['time'][0:-1])
nfd_entry_y = np.array(c['nfd_entry']['cpu_perc'])
nfd_entry_x = np.linspace(nfd_entry_orig.min(),nfd_entry_orig.max(),factor)
spl = make_interp_spline(nfd_entry_orig,nfd_entry_y,k=3)
nfd_entry_y = spl(nfd_entry_x)

fig,ax = plt.subplots()


ax.plot(sym_dec_x,sym_dec_y,label="Sym Dec")
ax.plot(sig_ver_x,sig_ver_y,label="Sig Ver")
ax.plot(avg_x,avg_y,label="Avg")
#ax.plot(nfd_entry_x,nfd_entry_y)

ax.legend(loc='upper left')

ax.set(xlabel="Time (seconds)",ylabel='CPU Usage %',title="Usage: "+out_file)

pylab.ylim([0,10])
ax.grid()
fig.savefig(out_file+".png")




