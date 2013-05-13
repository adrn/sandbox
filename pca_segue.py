# coding: utf-8

""" Perform PCA on the SEGUE data """

from __future__ import division, print_function

__author__ = "adrn <adrn@astro.columbia.edu>"

# Standard library
import os, sys

# Third-party
import numpy as np
from astropy.io import fits
from astropy.table import Table
import matplotlib.pyplot as plt

# Read in SEGUE data
catalog_file = "/Users/adrian/projects/segue-learn/data/ssppOut-dr9.fits"
hdulist = fits.open(catalog_file)
all_data = Table(hdulist[1].data)

# Annoyingly, there's no easy way to remove String-type columns so I can
#   convert the whole thing into a vanilla numpy ndarray...here's a hack
w, = np.where([all_data.columns[c].dtype.type == np.string_ for c in all_data.columns])
all_data.remove_columns([all_data.columns[ii].name for ii in w])

shp = (len(all_data),len(all_data.columns))

all_data = np.asarray(all_data) \
             .astype([(all_data.columns[ii].name,np.float64) for ii in range(len(all_data.columns))]) \
             .view(np.float64).reshape(shp)

hdulist.close()
del hdulist

# Now on to the PCA
A = all_data
Amean = np.mean(A.T,axis=1)
M = (A-Amean).T

cov = np.cov(M)
w, v = np.linalg.eig(cov)

N_eig = 10

M_rescaled = np.dot(v[:,:N_eig].T, M).T
A_proj = np.dot(v[:,:N_eig], M_rescaled.T).T + Amean

fig,axes = plt.subplots(3,3,figsize=(12,12))
axes[0,0].scatter(M_rescaled[:,0], M_rescaled[:,1])
axes[1,0].scatter(M_rescaled[:,0], M_rescaled[:,2])
axes[2,0].scatter(M_rescaled[:,0], M_rescaled[:,3])

axes[1,1].scatter(M_rescaled[:,1], M_rescaled[:,2])
axes[2,1].scatter(M_rescaled[:,1], M_rescaled[:,3])

axes[2,2].scatter(M_rescaled[:,2], M_rescaled[:,3])

plt.show()