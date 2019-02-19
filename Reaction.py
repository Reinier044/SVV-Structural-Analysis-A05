import numpy as np
from math import *

#given properties
La = 2.771 #m
D1 = 1.103/100 #m
D3 = 1.642/100 #m

E = 73.1*(10**9) #Pa
I = 0.3 #still to be changed moment of inertia
Izz = 0.2 #still to be changed moment of inertia around z-axis
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

#0 = -qy*(0.25*La-Ha/2)-pz*Ha/2+py*Ha/2-Pr*(cos(radians(26))*Ha/2-sin(radians(26))*Ha/2)

Pr = (qy*(0.25*La-Ha/2)+pz*Ha/2-py*Ha/2)/(cos(radians(26))*Ha/2-sin(radians(26))*Ha/2)
pry = Pr*sin(radians(26))
prz = Pr*cos(radians(26))
print(Pr)



#Reaction forces in y-direction and integration constants
#5 functions 5 unknows -> Moments around z-direction, sum of forces in y-direction
# and deflection function




a = np.array([[(x3-x1)**3/6,(x3-x2)**3/6,0,x3,1], [(x2-x1)**3/6,0,(x2-x3)**3/6,x2,1], [0,(x1-x2)**3/6,(x1-x3)**3/6,x1,1], [1,1,1,0,0], [-(x2-x1),0,(x3-x2),0,0]])
b = np.array([qy*x3**4/24+py*(x3-x2-xa/2)**3/6-pry*(x3-x2+xa/2)**3/6-E*Izz*D3,qy*x2**4/24+py*(-xa/2)**3/6-pry*(xa/2)**3/6,qy*x1**4/24+py*(x1-x2-xa/2)**3/6-pry*(x1-x2+xa/2)**3/6-E*Izz*D1,-py-qy*La+pry,py*xa/2+pry*xa/2])

y = np.linalg.solve(a,b)

R1y = y[0]
R2y = y[1]
R3y = y[2]
c1 = y[3]
c2 = y[4]

print(y)

#Reaction forces in z-direction and integration constants

c = np.array([[(x3-x1)**3/6,(x3-x2)**3/6,0,x3,1],[(x2-x1)**3/6,0,(x2-x3)**3/6,x2,1],[0,(x1-x2)**3/6,(x1-x3)**3/6,x1,1],[1,1,1,0,0],[x2-x1,0,-(x3-x2),0,0]])
d = np.array([-qz*x3**4/24+pz*(x3-x2-xa/2)**3/6-prz*(x3-x2+xa/2)**3/6 , -qz*x2**4/24+pz*(-xa/2)**3/6-prz*(xa/2)**3/6 , -qz*x1**4/24+pz*(x1-x2-xa/2)**3/6-prz*(x1-x2+xa/2)**3/6 , prz-pz+qz*La , -prz*xa/2-pz*xa/2])

z = np.linalg.solve(c,d)

R1z = z[0]
R2z = z[1]
R3z = z[2]
e1 = z[3]
e2 = z[4]

print(z)





















