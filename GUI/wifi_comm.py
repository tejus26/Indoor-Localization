
import serial
import matplotlib.pyplot as plt
import localization as lx
import time
import statistics as st
from mpl_toolkits.mplot3d import Axes3D
import sys
import telnetlib

import numpy as np

# Podium
#5.78 0.535 0.869

#Snack Table
#4.659 4.456 0.596

#Soda Table
#2.943 4.58 0.68

#Room Center
#2.655 2.015 0.891

#Refrigerator
#3.048 -0.634 1.891

def find_location(xs, ys, zs):
    dist_pod = (xs - 5.78)**2 + (ys - 0.535)**2 #+ (zs - 0.869)**2
    dist_snack = (xs - 4.659)**2 + (ys - 4.456)**2 #+ (zs - 0.596)**2
    dist_soda = (xs - 2.934)**2 + (ys - 4.58)**2 #+ (zs - 0.68)**2
    dist_center = (xs - 2.655)**2 + (ys - 2.015)**2 #+ (zs - 0.891)**2
    dist_refr = (xs - 3.048)**2 + (ys - (-0.639))**2 #+ (zs - 1.891)**2

    mind_dist = min(dist_pod, dist_snack, dist_soda, dist_center, dist_refr)
    if mind_dist > 0.5:
        return "I am here!"
    elif mind_dist == dist_pod:
        return "You are the presenter now, Good Luck!"
    elif mind_dist == dist_snack:
        return "Hungry? Snacks are here!"
    elif mind_dist == dist_soda:
        return "Thirsty? Coke's here!"
    elif mind_dist == dist_center:
        return "You are in the center of the room!"
    elif mind_dist == dist_refr:
        return "Looking for treasure? Open the door."
    return "I am here!"




def caliberate(x):
    if(x < 0.5):
        return 0.55
    elif (x < 1.3):
        return 0.6
    elif (x < 1.8):
        return 0.8
    elif(x < 2.3):
        return 0.83
    elif (x < 4):
        return 0.86
    else:
        return 0.98


a = 5

line_value1 = 0.0
line_value2 = 0.0
line_value3 = 0.0

#Adding 3D PLOT
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
c = 'b'
m = 'o'

ax.set_xlim3d(0, 8)
ax.set_ylim3d(0,6)
ax.set_zlim3d(0,3)
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.scatter(0.0, 0.0, 0.0, c=c, marker=m)
plt.pause(0.000000001)
plt.show()
tn = telnetlib.Telnet("192.168.240.1")

x_hist = []
y_hist = []
z_hist = []


while True:
    line1 = tn.read_until("\n")
    line2 = tn.read_until("\n")
    line3 = tn.read_until("\n")
    line4 = tn.read_until("\n")
    linelist = (line1, line2, line3, line4)
    line1 = sorted(linelist)[0]
    line2 = sorted(linelist)[1]
    line3 = sorted(linelist)[2]
    line4 = sorted(linelist)[3]

    print line1,
    print line2,
    print line3,
    print line4
    try:
        line1.split(' ') and line2.split(' ') and line3.split(' ') and line4.split(' ')
        id1, r1 = line1.split(' ')
        id2, r2 = line2.split(' ')
        id3, r3 = line3.split(' ')
        id4, r4 = line4.split(' ')
        if((id1 == 'FFFFFAFF') and (id2 == 'FFFFFBFF') and (id3 == 'FFFFFCFF') and (id4 == 'FFFFFDFF')):
            try:
                float(r1) and float(r2) and float(r3) #and float(r4)
                P=lx.Project(mode='3D', solver='LSE')

                P.add_anchor('FFFFFAFF', (0, 3.62, 2.34))
                P.add_anchor('FFFFFBFF', (0, 0, 0))
                P.add_anchor('FFFFFCFF', (0, 0, 2.34))
                P.add_anchor('FFFFFDFF', (4.86, 0, 2.34))

                #P.add_anchor('FFFFFAFF', (1.46, 4.88, 2.34))
                #P.add_anchor('FFFFFBFF', (7.10, 4.32 , 0.92))
                #P.add_anchor('FFFFFCFF', (0, 0, 0))
                #P.add_anchor('FFFFFDFF', (6.86, -1.22, 2.5))
                
                # P.add_anchor('FFFFFAFF', (0, 0, 0))
                # P.add_anchor('FFFFFBFF', (12, 0 , 0))
                # P.add_anchor('FFFFFCFF', (10, 5, 3))
                # P.add_anchor('FFFFFDFF', (8, 5, -2))
                t,label=P.add_target()
                r1 = float(r1)
                r2 = float (r2)
                r3 = float(r3)
                r4 = float (r4)
                r1 = r1 - caliberate(r1)
                r2 = r2 - caliberate(r2)
                r3 = r3 - caliberate(r3)
                r4 = r4 - caliberate(r4)
                print id1, r1, 
                print id2, r2, 
                print id3, r3, 
                print id4, r4, 
                t.add_measure(id1, r1)
                t.add_measure(id2, r2)
                t.add_measure(id3, r3)
                t.add_measure(id4, r4)
                try:
                    P.solve()
                    if len(x_hist)>5:
                        x_hist.pop()
                        y_hist.pop()
                        z_hist.pop()
                    print len(x_hist)
                    x_hist.insert(0,t.loc.x);
                    y_hist.insert(0,t.loc.y);
                    z_hist.insert(0,t.loc.z);
                    rob_x = st.median(x_hist)
                    rob_y = st.median(y_hist)
                    rob_z = st.median(z_hist)
                    print round(rob_x, 3),
                    print round(rob_y, 3),
                    print round(rob_z,3)
                    xs = round(rob_x, 3)
                    ys = round(rob_y, 3)
                    zs = round(rob_z, 3)
                    #plt.cla()
                    ax.set_xlim3d(0, 12)
                    ax.set_ylim3d(0,12)
                    ax.set_zlim3d(0,12)
                    ax.set_xlabel('X axis')
                    ax.set_ylabel('Y axis')
                    ax.set_zlabel('Z axis')
                    ax.scatter(xs, ys, zs, c=c, marker=m); #ax.text(xs, ys, zs, find_location(xs, ys, zs))
                    plt.pause(0.000000001)
                    plt.show()
                    tn.read_very_eager()
                except AttributeError:
                    a = a + 1
            except ValueError:
                a = a + 1
    except ValueError:
        a = a + 1
