# Orbitals

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math

def Lag(x, n, l):
    k = 2*l+1
    m = n+l
    
    if m == 0:
        return 1.
    elif m == 1:
        return -x + k + 1
    elif m == 2:
        return 0.5 * (x**2 - 2.*(k+2.)*x + (k+1)*(k+2.))
    elif m == 3:
        return (1./6.) * (-x**3 + 3*(k+3)*x**2 - 3*(k+2)*(k+3)*x + (k+1)*(k+2)*(k+3))    
    else:
        raise ValueError("Currently only supports n+l <= 3")

def R_nl(r, n, l, Z=1):
    if (n+l) > 3:
        raise ValueError("Currently only supports n+l <= 3")
        
    A = -np.sqrt(Z*math.factorial(n-l-1) / (n**2 * math.factorial(n+l)**3))
    B = np.exp(-r / 2.) * r**(l+1) * Lag(r, n, l)
    
    return A*B

r = np.linspace(0.01, 10., 100000)
phi = np.random.uniform(0.0, 2.*np.pi, len(r))
theta = np.arccos(2.*np.random.uniform(0.0, 1., len(r)) - 1.)

Rs = R_nl(r, 2, 1)**2
x = Rs*np.sin(theta)*np.sin(phi)
y = Rs*np.sin(theta)*np.cos(phi)
z = Rs*np.cos(phi)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z, 'k.', alpha=0.3)

plt.show()