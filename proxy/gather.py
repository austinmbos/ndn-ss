"""
process the data from dockercpu.dat
"""



from scipy.interpolate import make_interp_spline, BSpline
import statistics as stat
import matplotlib.pyplot as plt
import pylab
import json
import numpy as np

factor = 30

with open("dockercpu.dat","r") as f:
    c = json.load(f)

sym_dec_orig = np.array(c['sym_dec']['time'][0:-1])
sym_dec_y = np.array(c['sym_dec']['cpu_perc'])
sym_dec_x = np.linspace(sym_dec_orig.min(),sym_dec_orig.max(),factor)
spl = make_interp_spline(sym_dec_orig,sym_dec_y,k=3)
sym_dec_y = spl(sym_dec_x)

sig_ver_orig = np.array(c['sig_ver']['time'][0:-1])
sig_ver_y = np.array(c['sig_ver']['cpu_perc'])
sig_ver_x = np.linspace(sig_ver_orig.min(),sig_ver_orig.max(),factor)
spl = make_interp_spline(sig_ver_orig,sig_ver_y,k=3)
sig_ver_y = spl(sig_ver_x)

nfd_entry_orig = np.array(c['nfd_entry']['time'][0:-1])
nfd_entry_y = np.array(c['nfd_entry']['cpu_perc'])
nfd_entry_x = np.linspace(nfd_entry_orig.min(),nfd_entry_orig.max(),factor)
spl = make_interp_spline(nfd_entry_orig,nfd_entry_y,k=3)
nfd_entry_y = spl(nfd_entry_x)

fig,ax = plt.subplots()


ax.plot(sym_dec_x,sym_dec_y)
ax.plot(sig_ver_x,sig_ver_y)
ax.plot(nfd_entry_x,nfd_entry_y)


pylab.ylim([0,2])
ax.grid()
fig.savefig("test.png")




