#!/usr/bin/env python

__author__ = 'apw'

# Standard library dependencies
import os, sys
import sys

# Third-party imports
import numpy as np
import sqlalchemy
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from math import radians

# Custom modules
from spectradb.HydraDR9dbConnection import db
from spectradb.BOSSModelClasses import *
from spectradb.SDSSModelClasses import *

# Query to get all SDSS-I and -II "good" plates
sdssPlateCenters = db.Session.query(Pointing.center_ra, Pointing.center_dec).\
                          join(Design, Plate, SDSSSpectrumHeader, SDSSPlateQuality).\
                          filter(SDSSPlateQuality.label == "good").\
                          all()

# Query to get all "good" BOSS plates from before July 2011 (DR9)
bossDR9PlateCenters = db.Session.query(Pointing.center_ra, Pointing.center_dec).\
                          join(Design, Plate, BOSSSpectrumHeader, BOSSPlateQuality).\
                          filter(BOSSSpectrumHeader.mjd <= 55811).\
                          filter(BOSSPlateQuality.label == "good").\
                          all()

# Create a figure and axis with an aitoff projection
fig = plt.figure(figsize=(15,10))
ax = fig.add_subplot(111, projection="aitoff")                          

for ii,(ra,dec) in enumerate(sdssPlateCenters):
    # For the first plate, add a label to be used for the legend
    if ii == 0: cir = Circle((radians(-(ra-180)),radians(dec)), radius=radians(1.5), facecolor='b', ec="None", alpha=0.3, label="SDSS-I,-II ('good')")
    else: cir = Circle((radians(-(ra-180)),radians(dec)), radius=radians(1.5), facecolor='b', ec="None", alpha=0.3)
    ax.add_patch(cir)
    
for ii,(ra,dec) in enumerate(bossDR9PlateCenters):
    # For the first plate, add a label to be used for the legend
    if ii == 0: cir = Circle((radians(-(ra-180)),radians(dec)), radius=radians(1.5), facecolor='r', ec="None", alpha=0.3, label="BOSS DR9")
    else: cir = Circle((radians(-(ra-180)),radians(dec)), radius=radians(1.5), facecolor='r', ec="None", alpha=0.3)
    ax.add_patch(cir)

# Add a grid to the plot    
ax.grid()

# Matplotlib doesn't allow changing the axis limits on a projected plot, so we have to do this ourselves...
ax.set_xticklabels([330, 300, 270, 240, 210, 180, 150, 120, 90, 60, 30])
fig.suptitle("BOSS DR9 Plate Coverage")
ax.legend()

plt.savefig("boss_dr9.png", dpi=100)
#or, for a pdf: plt.savefig("boss_dr9.pdf")
