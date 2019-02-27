import numpy as np
from math import *
import matplotlib.pyplot as plt

#given properties
La = 2.771 #m
ca = 0.547 #m
D1 = 1.103/100 #m
d1y = D1*cos(radians(26))
d1z = D1*sin(radians(26))
D3 = 1.642/100 #m
d3y = D3*cos(radians(26))
d3z = D3*sin(radians(26))

E = 73.1*(10**9) #Pa
Izz = 5.2*(10**(-5))
Iyy = 1.92*(10**(-4))
x1 = 0.153 #m 
x2 = 1.281 #m
x3 = 2.681 #m
xa = 28.0/100 #m
Ha = 22.5/100 #m

P = 91.7*1000 #N
py = P*sin(radians(26)) #N
pz = P*cos(radians(26)) #N
q = 4.53*1000 #N/m
qy = q*cos(radians(26)) #N
qz = q*sin(radians(26)) #N

Pr = (qy*(0.25*ca-Ha/2)+pz*Ha/2-py*Ha/2)/(cos(radians(26))*Ha/2-sin(radians(26))*Ha/2)
pry = Pr*sin(radians(26))
prz = Pr*cos(radians(26))

# and deflection function
a = np.array([[0,0,0,x1,1], [-(x2-x1)**3/6,0,0,x2,1], [-(x3-x1)**3/6,-(x3-x2)**3/6,0,x3,1], [1,1,1,0,0], [x1,x2,x3,0,0]])
b = np.array([-E*Izz*d1y-qy*x1**4/24,
              pry*(xa/2)**3/6-qy*x2**4/24,
              -E*Izz*d3y-py*(x3-x2-xa/2)**3/6-qy*x3**4/24+pry*(x3-x2+xa/2)**3/6,
              qy*La+py-pry,
              qy*La**2/2+py*(x2+xa/2)-pry*(x2-xa/2)])
y = np.linalg.solve(a,b)
R1y = y[0]
R2y = y[1]
R3y = y[2]
c1 = y[3]
c2 = y[4]

#Reaction forces in z-direction and integration constants

c = np.array([[0,0,0,x1,1],[(x2-x1)**3/6,0,0,x2,1],[(x3-x1)**3/6,(x3-x2)**3/6,0,x3,1],[1,1,1,0,0],[x1,x2,x3,0,0]])
d = np.array([-E*Iyy*d1z-qz*x1**4/24,
              -qz*x2**4/24-prz*(xa/2)**3/6 ,
              -qz*x3**4/24+pz*(x3-x2-xa/2)**3/6-prz*(x3-x2+xa/2)**3/6 - E*Iyy*d3z ,
              -prz+pz-qz*La ,
              -qz*La**2/2+pz*(x2+xa/2)-prz*(x2-xa/2)])
z = np.linalg.solve(c,d)

R1z = z[0]
R2z = z[1]
R3z = z[2]
e1 = z[3]
e2 = z[4]
#check

t1 = R1y + R2y + R3y + pry - py - qy*La
t2 = R1z + R2z + R3z + prz - pz + qz*La

#Ranges

section = 1000
s1 = np.arange(0,x1,0.0255)
s2 = np.arange(x1,x2-xa/2,0.0247)
s3 = np.arange(x2-xa/2,x2,0.024522)
s4 = np.arange(x2,x2+xa/2,0.024522)
s5 = np.arange(x2+xa/2,x3,0.024706)
s6 = np.arange(x3,La,0.024522)

def lijst(x):
    m = []
    for i in x:
        m.append(i)
    return m

#Moment diagram x-y plane

my1 = qy/2*s1**2
my2 = qy/2*(s2)**2 - R1y*(s2-x1)
my3 = qy/2*(s3)**2 - R1y*(s3-x1) - pry*(s3-(x2-xa/2))
my4 = qy/2*(s4)**2 - R1y*(s4-x1) - pry*(s4-(x2-xa/2)) - R2y*(s4-x2)
my5 = qy/2*(s5)**2 - R1y*(s5-x1) - pry*(s5-(x2-xa/2)) - R2y*(s5-x2) + py*(s5-(x2+xa/2))
my6 = qy/2*(s6)**2 - R1y*(s6-x1) - pry*(s6-(x2-xa/2)) - R2y*(s6-x2) + py*(s6-(x2+xa/2)) - R3y*(s6-x3)

m1 = lijst(my1)
m2 = lijst(my2)
m3 = lijst(my3)
m4 = lijst(my4)
m5 = lijst(my5)
m6 = lijst(my6)

MZ = m1+m2+m3+m4+m5+m6

#Shear diagram x-y plane
vy1 = -qy*s1
vy2 = -qy*s2 + R1y
vy3 = -qy*s3 + R1y + pry
vy4 = -qy*s4 + R1y + pry + R2y
vy5 = -qy*s5 + R1y + pry + R2y - py
vy6 = -qy*s6 + R1y + pry + R2y - py + R3y

v11 = lijst(vy1)
v22 = lijst(vy2)
v33 = lijst(vy3)
v44 = lijst(vy4)
v55 = lijst(vy5)
v66 = lijst(vy6)

VY = v11+v22+v33+v44+v55+v66

#Moment diagram x-z plane

mz1 = qz/2*s1**2
mz2 = qz/2*(s2)**2 + R1z*(s2-x1)
mz3 = qz/2*(s3)**2 + R1z*(s3-x1) + prz*(s3-(x2-xa/2))
mz4 = qz/2*(s4)**2 + R1z*(s4-x1) + prz*(s4-(x2-xa/2)) + R2z*(s4-x2)
mz5 = qz/2*(s5)**2 + R1z*(s5-x1) + prz*(s5-(x2-xa/2)) + R2z*(s5-x2) - pz*(s5-(x2+xa/2))
mz6 = qz/2*(s6)**2 + R1z*(s6-x1) + prz*(s6-(x2-xa/2)) + R2z*(s6-x2) - pz*(s6-(x2+xa/2)) + R3z*(s6-x3)

m11 = lijst(mz1)
m22 = lijst(mz2)
m33 = lijst(mz3)
m44 = lijst(mz4)
m55 = lijst(mz5)
m66 = lijst(mz6)

MY = m11+m22+m33+m44+m55+m66

#Shear diagram x-z plane

vz1 = qz*s1
vz2 = qz*s2 + R1z
vz3 = qz*s3 + R1z + prz
vz4 = qz*s4 + R1z + prz + R2z
vz5 = qz*s5 + R1z + prz + R2z - pz
vz6 = qz*s6 + R1z + prz + R2z - pz + R3z

v1 = lijst(vz1)
v2 = lijst(vz2)
v3 = lijst(vz3)
v4 = lijst(vz4)
v5 = lijst(vz5)
v6 = lijst(vz6)

VZ = v1+v2+v3+v4+v5+v6

#torsion diagram (moment around shear center with x_(shear center) = ca - 0.4324 m as seen from the leading edge)

t1 = -qy*s1*(0.25*ca-(ca -0.4324))
t2 = -qy*s2*(0.25*ca-(ca -0.4324))
t3 = -qy*s3*(0.25*ca-(ca -0.4324)) - pry*(ca -0.4324) + prz*Ha/2
t4 = -qy*s4*(0.25*ca-(ca -0.4324)) - pry*(ca -0.4324) + prz*Ha/2
t5 = -qy*s5*(0.25*ca-(ca -0.4324)) - pry*(ca -0.4324) + prz*Ha/2 + py*(ca -0.4324) - pz*Ha/2
t6 = -qy*s6*(0.25*ca-(ca -0.4324)) - pry*(ca -0.4324) + prz*Ha/2 + py*(ca -0.4324) - pz*Ha/2

t11 = lijst(t1)
t22 = lijst(t2)
t33 = lijst(t3)
t44 = lijst(t4)
t55 = lijst(t5)
t66 = lijst(t6)

#list with torsion for predefined x-values
T = t11 + t22 + t33 + t44 + t55 + t66

#plotting diagrams

#moment x-y plane
plt.subplot(5,1,1)
plt.title('my')
plt.plot(s1,my1,s2,my2,s3,my3,s4,my4,s5,my5,s6,my6)

#shear x-y plane
plt.subplot(5,1,2)
plt.title('vy')
plt.plot(s1,vy1,s2,vy2,s3,vy3,s4,vy4,s5,vy5,s6,vy6)

#moment x-z plane
plt.subplot(5,1,3)
plt.title('mz')
plt.plot(s1,mz1,s2,mz2,s3,mz3,s4,mz4,s5,mz5,s6,mz6)

#shear x-z plane
plt.subplot(5,1,4)
plt.title('vz')
plt.plot(s1,vz1,s2,vz2,s3,vz3,s4,vz4,s5,vz5,s6,vz6)

#torsion diagram
plt.subplot(5,1,5)
plt.title('torsion')
plt.plot(s1,t1,s2,t2,s3,t3,s4,t4,s5,t5,s6,t6)
plt.show()

#Moment around z calculator in function of x
def Momenty(x):
    Moment = 0
    if x > 0 and x<=x1 :
        Moment = qy/2*x**2
    if x > x1 and x<=(x2-xa/2):
        Moment = qy/2*(x)**2 - R1y*(x-x1)
    if x > (x2-xa/2) and x <= x2:
        Moment = qy/2*(x)**2 - R1y*(x-x1) - pry*(x-(x2-xa/2))
    if x > x2 and x <= x2+xa/2:
        Moment = qy/2*(x)**2 - R1y*(x-x1) - pry*(x-(x2-xa/2)) - R2y*(x-x2)
    if x > x2+xa/2 and x <= x3:
        Moment = qy/2*(x)**2 - R1y*(x-x1) - pry*(x-(x2-xa/2)) - R2y*(x-x2) + py*(x-(x2+xa/2))
    if x > x3 and x <= La:
        Moment = qy/2*(x)**2 - R1y*(x-x1) - pry*(x-(x2-xa/2)) - R2y*(x-x2) + py*(x-(x2+xa/2)) - R3y*(x-x3)
    return Moment

#deflection in local y in function of x
def deflection(x):
    deflection = 0
    if x > 0 and x<=x1:
        deflection = -(qy/24.*x**4 + c1*x + c2)/(E*Izz)
    if x > x1 and x<=(x2-xa/2):
        deflection = -(qy/24.*x**4 + c1*x + c2 - R1y*(x-x1)**3/6)/(E*Izz)
    if x > (x2-xa/2) and x <= x2:
        deflection = -(qy/24.*x**4 + c1*x + c2 - R1y*(x-x1)**3/6 - pry*(x-(x2-xa/2))**3/6)/(E*Izz)
    if x > x2 and x <= x2+xa/2:
        deflection = -(qy/24.*x**4 + c1*x + c2 - R1y*(x-x1)**3/6 - pry*(x-(x2-xa/2))**3/6 - R2y*(x-x2)**3/6)/(E*Izz)
    if x > x2+xa/2 and x <= x3:
        deflection = -(qy/24.*x**4 + c1*x + c2 - R1y*(x-x1)**3/6 - pry*(x-(x2-xa/2))**3/6 - R2y*(x-x2)**3/6 + py*(x-(x2+xa/2))**3/6)/(E*Izz)
    if x > x3 and x <= La:
        deflection = -(qy/24.*x**4 + c1*x + c2 - R1y*(x-x1)**3/6 - pry*(x-(x2-xa/2))**3/6 - R2y*(x-x2)**3/6 + py*(x-(x2+xa/2))**3/6 - R3y*(x-x3)**3/6)/(E*Izz)
    return deflection

#torsion in function of x
def torsion(x):
    torsion = 0
    if x > 0 and x <= (x2 - xa/2):
        torsion = -qy*x*(0.25*ca - (ca - 0.4324))
    if x > (x2-xa/2) and x <= (x2 + xa/2):
        torsion = -qy*x*(0.25*ca - (ca - 0.4324)) - pry*(ca - 0.4324) + prz* Ha/2
    if x > (x2 + xa/2) and x < La:
        torsion = -qy*x*(0.25*ca - (ca - 0.4324)) - pry*(ca - 0.4324) + prz* Ha/2 + py*(ca - 0.4324) - pz* Ha/2
    return torsion

#smooth lined x and y -plot for Moment diagram.
xplot = np.arange(0,La,0.02452)
yplot = []
ydeflection = []
torsionalongx = []
Mz = []

for i in lijst(xplot):
    yplot.append(Momenty(i))
    ydeflection.append(deflection(i))
    torsionalongx.append(torsion(i))
    Mz.append(Momenty(i))
plt.show()

