import serial
import matplotlib.pyplot as plt
import localization as lx
import time
from mpl_toolkits.mplot3d import Axes3D

import numpy as np

#x-axis_max = 7.10
#y-axis_max = 4.32
#z-axis_max = 

#Left fixture back
#Ax =  1.46 
#Ay = 4.88
#Az = 2.34

# Table corner
#Bx = 7.10
#By = 4.32
#Bz = 0.92

#Origin, back door
#Cx = 0
#Cy = 0
#Cz = 0


#Above exit sign
#Dx = 7.1 - 0.24
#Dy = -1.22
#Dz = 2.5

# 0.25
# 0.75
# 1.52
# 2
# 3.04
# 4.56
# 6.08


# 0.55
# 0.55
# 0.83
# 0.85
# 0.91
# 0.79
# 0.92
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

ax.set_xlim3d(0, 12)
ax.set_ylim3d(0,12)
ax.set_zlim3d(0,12)
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.scatter(0.0, 0.0, 0.0, c=c, marker=m)
plt.pause(0.000000001)
plt.show()
with serial.Serial('/dev/ttyACM0', 115200, timeout=1) as ser:
    while True:

        # print "Hello\n"
        ser.flushInput()
        line1 = ser.readline()
        line2 = ser.readline()
        line3 = ser.readline()
        line4 = ser.readline()

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


            
            if((len(id1) == 8) and (len(id2) == 8) and (len(id3) == 8) and (len(id4) == 8)):
                try:
                    float(r1) and float(r2) and float(r3) #and float(r4)
                    P=lx.Project(mode='3D', solver='LSE_GC')

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
                    # start = time.time()
		    try:
			    P.solve()
			    # end = time.time()
			    # print (end - start)
			    # print r1, 
			    # print id1
			    # print r2, 
			    # print id2
			    # print r3, 
			    # print id3
			    # print r4,
			    # print id4
			    # print "************"
			    # plt.gcf().clear()
			    print round(t.loc.x, 3),
			    print round(t.loc.y, 3),
			    print round(t.loc.z,3)
			    xs = round(t.loc.x, 3)
			    ys = round(t.loc.y, 3)
			    zs = round(t.loc.z, 3)
			    plt.cla()
			    ax.set_xlim3d(0, 12)
			    ax.set_ylim3d(0,12)
			    ax.set_zlim3d(0,12)
			    ax.set_xlabel('X axis')
			    ax.set_ylabel('Y axis')
			    ax.set_zlabel('Z axis')


			    ax.scatter(xs, ys, zs, c=c, marker=m)
			    plt.pause(0.000000001)
			    plt.show()
		    except AttributeError:
			a = a + 1

                except ValueError:
                    a = a + 1
        except ValueError:
            a = a + 1
ser.close()
