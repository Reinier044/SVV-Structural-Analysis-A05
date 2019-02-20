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
Izz = 11996389.06*(10**(-12)) #still to be changed moment of inertia around z-axis
Iyy = 52013464.25*(10**(-12))
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


#Moment around x-axis find reaction force actuator

#0 = -qy*(0.25*ca-Ha/2)-pz*Ha/2+py*Ha/2+Pr*(cos(radians(26))*Ha/2-sin(radians(26))*Ha/2)

Pr = (qy*(0.25*ca-Ha/2)+pz*Ha/2-py*Ha/2)/(cos(radians(26))*Ha/2-sin(radians(26))*Ha/2)
pry = Pr*sin(radians(26))
prz = Pr*cos(radians(26))
print(Pr)



#Reaction forces in y-direction and integration constants
#5 functions 5 unknows -> Moments around z-direction, sum of forces in y-direction
# and deflection function




a = np.array([[0,0,0,x1,1], [-(x2-x1)**3/6,0,0,x2,1], [-(x3-x1)**3/6,-(x3-x2)**3/6,0,x3,1], [1,1,1,0,0], [-(x2-x1),0,(x3-x2),0,0]])
b = np.array([-E*Izz*d1y-qy*x1**4/24,
              pry*(xa/2)**3/6-qy*x2**4/24,
              -E*Izz*d3y-py*(x3-x2-xa/2)-qy*x3**4/24+pry*(x3-x2+xa/2),
              qy*La+py-pry,
              py*xa/2+pry*xa/2])

y = np.linalg.solve(a,b)

R1y = y[0]
R2y = y[1]
R3y = y[2]
c1 = y[3]
c2 = y[4]

print(y)

#Reaction forces in z-direction and integration constants

c = np.array([[(x3-x1)**3/6,(x3-x2)**3/6,0,x3,1],[(x2-x1)**3/6,0,(x2-x3)**3/6,x2,1],[0,(x1-x2)**3/6,(x1-x3)**3/6,x1,1],[1,1,1,0,0],[x2-x1,0,-(x3-x2),0,0]])
d = np.array([-E*Iyy*d1z-qz*x1**4/24,
              -qz*x2**4/24-prz*(xa/2)**3/6 ,
              -qz*x3**4/24+pz*(x3-x2-xa/2)**3/6-prz*(x3-x2+xa/2)**3/6 ,
              -prz+pz-qz*La ,
              -prz*xa/2-pz*xa/2])

z = np.linalg.solve(c,d)

R1z = z[0]
R2z = z[1]
R3z = z[2]
e1 = z[3]
e2 = z[4]

print(z)


#Ranges

s1 = np.arange(0,x1,0.001)
s2 = np.arange(x1,x2-xa/2,0.001)
s3 = np.arange(x2-xa/2,x2,0.001)
s4 = np.arange(x2,x2+xa/2,0.001)
s5 = np.arange(x2+xa/2,x3,0.001)
s6 = np.arange(x3,La,0.001)

#Moment diagram x-y plane

m1 = qy/2*s1**2
m2 = qy/2*(s2)**2 - R1y*(s2-x1)
m3 = qy/2*(s3)**2 - R1y*(s3-x1) - pry*(s3-(x2-xa/2))
m4 = qy/2*(s4)**2 - R1y*(s4-x1) - pry*(s4-(x2-xa/2)) - R2y*(s4-x2)
m5 = qy/2*(s5)**2 - R1y*(s5-x1) - pry*(s5-(x2-xa/2)) - R2y*(s5-x2) + py*(s5-(x2+xa/2))
m6 = qy/2*(s6)**2 - R1y*(s6-x1) - pry*(s6-(x2-xa/2)) - R2y*(s6-x2) + py*(s6-(x2+xa/2)) - R3y*(s6-x3)

plt.subplot(2,1,1)
plt.plot(s1,m1,s2,m2,s3,m3,s4,m4,s5,m5,s6,m6)


#Shear diagram x-y plane

v1 = -q*s1
v2 = -q*s2 + R1y
v3 = -q*s3 + R1y + pry
v4 = -q*s4 + R1y + pry + R2y
v5 = -q*s5 + R1y + pry + R2y - py
v6 = -q*s6 + R1y + pry + R2y - py + R3y

plt.subplot(2,1,2)
plt.plot(s1,v1,s2,v2,s3,v3,s4,v4,s5,v5,s6,v6)

plt.show()























