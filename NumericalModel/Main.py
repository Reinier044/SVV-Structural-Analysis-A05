#Import stuff
import numpy as np
import matplotlib.pyplot as plt

#Variables
sections = 6

#Geometric constants
la = 2771.
t1 = 1.1
t2 = 2.9
Ca = 547.
h = 225.
G = 28000.

#Calculation constants
r = h/2
A1 = (h/2)**2*np.pi
A2 = (Ca-r)*r
s1 = np.pi*r
s2 = 2*np.sqrt(r**2+(Ca-r)**2)
dstr = (s1+s2)/19
tht2 = dstr/r
tht1 = np.pi/2-tht2
phi = np.tan(r/(Ca-r))
p_tr = np.sin(np.pi/2-phi)*r

#Given data from Luc and Andreas
Vz = np.array([67290.91180274,67290.91180274,67290.91180274,67290.91180274,67290.91180274,67290.91180274])
Vy = np.array([-23344.02874676,-23344.02874676,-23344.02874676,-23344.02874676,-23344.02874676,-23344.02874676])
T = np.array([5000000.,5000000.,5000000.,5000000.,5000000.,5000000.])
Mo = np.array([5000000.,5000000.,5000000.,5000000.,5000000.,5000000.])

#Given data from Angela
Iyy = 52013464.25
Izz = 11996389.06
Area = np.array([0,103.71,103.71,103.71,103.71,103.71,103.71,103.71,182.19,129.75,106.83,129.75,182.19,103.71,103.71,103.71,103.71,103.71,103.71,103.71])
zloc = np.array([0,54.31,108.62,162.93,217.24,271.55,325.86,380.17,434.48,514,547,514,434.48,380.17,325.86,271.55,217.24,162.93,108.62,54.31])
yloc = np.array([0.,-14.0625,-28.125,-42.1875,-56.25,-70.3125,-84.375,-98.4375,-112.5,-79.55,0.,79.55,112.5,98.4375,84.375,70.3125,56.25,42.1875,28.125,14.0625])

#Empty arrays
Tdefl = np.zeros(sections)
Sdefl = np.zeros(sections)
qby = np.zeros(sections)
qbz = np.zeros(sections)
qb = np.zeros([20,sections])
qs01 = np.zeros(sections)
qs02 = np.zeros(sections)
qsum1 = np.zeros(sections)
qsum2 = np.zeros(sections)

#Deflection due to Torque (x-axis)
for i in range(0,sections):
    eqn = np.array([[2*A1,2*A2,0],[(s1/t1+h/t2)/(2*A1*G),-h/(2*A1*G*t2),-1],[-h/(2*A2*G*t2),(s2/t1+h/t2)/(2*A2*G),-1]])
    sol = np.array([[T[i]],[0],[0]])
    x = np.linalg.solve(eqn,sol)*la/sections
    Tdefl[i] = x[2]+Tdefl[i-1]
    qs01[i] = x[0]
    qs02[i] = x[1]


#Calculation of shear flows
for i in range(0,sections):
    qby[i] = -Vz[i]/Iyy
    qbz[i] = -Vy[i]/Izz
    qb[0][i] = qby[i]*Area[8]*zloc[8]+qbz[i]*Area[8]*yloc[8]
    qb[7][i] = 0.
    qb[8][i] = 0.
    qb[9][i] = qby[i]*Area[9]*zloc[9]+qbz[i]*Area[9]*yloc[9]
    qb[19][i] = qby[i]*Area[1]*zloc[1]+qbz[i]*Area[1]*yloc[1]
    for j in range(1,7):
        qb[j][i] = qby[i]*Area[j]*zloc[j]+qbz[i]*Area[j]*yloc[j]
    for j in range(10,19):
        qb[j][i] = qb[19-j][i]
    for j in range(8,12):
        qsum1[i] = (qb[j][i]*dstr)/t1+qsum1[i-1]
    for j in range(1,8):
        qsum2[i] = 2*(qb[j][i]*dstr)/t1+qsum2[i-1]

#Deflection due to shear
for i in range(0,sections):
    Mo_nose =2*qb[8][i]*r**2*tht1+2*qb[9][i]*r**2*tht2
    Mo_triangle = 2*(qb[7][i]+qb[6][i]+qb[5][i]+qb[4][i]+qb[3][i]+qb[2][i]+qb[1][i])*p_tr*dstr+qb[19][i]*p_tr*dstr
    eqn = np.array([[2*A1,2*A2,0],[(s1/t1+h/t2)/(2*A1),-h/(2*A1*t2),-1],[-h/(2*A2*t2),(h/t2+s1/t1)/(2*A2),-1]])
    sol = np.array([[-Mo_nose-Mo_triangle-Mo[i]],[(-qsum1[i]-qb[0][i]*h/t2)/(2*A1*G)],[(-qsum2[i]-qb[0][i]*h/t2)/(2*A1*G)]])
    x2 = np.linalg.solve(eqn,sol)*la/sections
    Sdefl[i] = x2[2]+Sdefl[i-1]
    for j in range(1,8):
        qb[j][i] = qb[j][i]+x2[0]+qs01[i]
    for j in range(8,12):
        qb[j][i] = qb[j][i]+x2[1]+qs02[i]
    for j in range(12,19):
        qb[j][i] = qb[19-j][i]
    qb[0][i] = qb[0][i]+x[0]+qs01[i]
    qb[19][i] = qb[19][i]+x[0]+qs01[i]


#Deflection due to bending (z-axis)
#Andreas

#Deflection total
Ley = np.zeros(sections)
Tey = np.zeros(sections)
for i in range(0,sections):
    Ley[i] = -np.sin(Tdefl[i])*h/2+np.sin(Sdefl[i])*la/sections#+Mdefl
    Tey[i] = np.sin(Tdefl[i])*(Ca-h/2)+np.sin(Sdefl[i])*la/sections#+Mdefl

#Plotting
im = plt.imread("Figure2.png")
implot = plt.imshow(im)
y = [265,340,350,360,370,380,390,390,380,310,230,160,140,140,150,160,170,180,190,200]
z = [210,570,510,450,390,330,270,210,150,100,90,130,190,250,310,370,430,490,550,650]
for i in range(20):
    plt.annotate(qb[i,0],(z[i],y[i]))
plt.xlabel("z")
plt.ylabel("y")
plt.title("Shear flows")
plt.show()