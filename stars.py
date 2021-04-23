#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 11:03:15 2021

@author: RayG
"""


import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.lines as mlines
import pandas as pd
import matplotlib.animation as animation
plt.style.use('dark_background')

#%%

# Import data using pandas
headers = ['tech','com','appmag','dist','absmag','color','nbl']
data = pd.read_csv('stars.csv',names=headers,skiprows=1)

# Draw an HR diagram marking the different "types" of stars
fig1 = plt.figure(figsize=(6,8))
ax1 = plt.subplot(111)

plt.plot(data[data['nbl'] == 'Bright']['color'],data[data['nbl'] == 'Bright']['absmag'],
         markersize=2,marker='.',linestyle='None',label='Bright')
plt.plot(data[data['nbl'] == 'Near']['color'],data[data['nbl'] == 'Near']['absmag'],
         markersize=2,marker='.',linestyle='None',label='Near')
plt.plot(data[data['nbl'] == 'Luminous']['color'],data[data['nbl'] == 'Luminous']['absmag'],
         markersize=2,marker='.',linestyle='None',label='Luminous')
plt.plot(data[data['nbl'] == 'Both']['color'],data[data['nbl'] == 'Both']['absmag'],
         markersize=2,marker='.',linestyle='None',label='Both Bright & Near')
plt.xlabel(r'$B-V$')
plt.ylabel(r'$V$')
plt.xlim(-0.5,2.5)
plt.gca().invert_yaxis()
plt.legend(loc='best')
plt.tight_layout()

#%%

# Set up the plot for the animation
fig2 = plt.figure(figsize=(6,8))
ax2 = plt.subplot(111)
ax2.set_xlim(-0.5,2.5)
ax2.set_ylim(-11,20)
ax2.invert_yaxis()
ax2.set_xlabel(r'$B-V$')
ax2.set_ylabel(r'$M_V$')

# Set up frames so that there is a 1 second pause at the beginning and end
frames_a = list(np.zeros(1000//20))
frames_b = list(np.linspace(0,1,100))
frames_c = list(np.ones(1000//20))

frames_a.extend(frames_b)
frames_a.extend(frames_c)

# Set up the points that the stars will move between
old_points = np.asarray([data['color'], data['appmag']])
new_points = np.asarray([data['color'], data['absmag']])

# Define the animation command
# The variable interpolation calculates where the stars will move 
# set_offsets() moves the stars
# set_color() gives them all blue/red colors corresponding to their B-V color
def move(i):
    interpolation = old_points*(1-i) + new_points*i
    stuff.set_offsets(interpolation.T)
    stuff.set_color(cmap(norm(data['color'])))
    return stuff,

# Set up the points and colormap
stuff = plt.scatter([],[],s=3,marker='.',linestyle='None')
cmap = matplotlib.cm.coolwarm
norm = matplotlib.colors.Normalize(vmin=-0.5, vmax=2.5)

# Run the animation
anim = FuncAnimation(fig2, move, 
                     frames = frames_a, interval = 20, blit=True, repeat=False, save_count=200)
plt.show()
# Uncomment the next line to save the animation as a gif
# Note: it will not save the 1 second pauses at the beginning and end of the animation
# anim.save('stars_hr.gif')
