import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LightSource

#-------------------------------------------------

def mse(y,y_pred):
    return np.mean((y-y_pred)**2)

def model(w0, w1, x):
    y = w1*x + w0
    return y

def lasso_error(w0, w1, x_true, y_true, alpha=1.0):
    y_pred = model(w0, w1, x)
    error = mse(y_true,y_pred) + alpha*( abs(w0)+abs(w1) )
    return error

#-------------------------------------------------

# generate noisy data on a line:
w0    = 25.0 # intercept
w1    = 0.0 # slope
num_samples = 150
x     = np.random.randn(num_samples)
noise = np.random.randn(num_samples) * 0.4
y = w1*x + w0 + noise

# calculate error for many pairs of w0 and w1
limit = 50
num_samples = 100
X = np.linspace(start=-limit, stop=limit, num=num_samples)
Y = np.linspace(start=-limit, stop=limit, num=num_samples)
X, Y = np.meshgrid(X, Y)
Z = np.zeros_like(X)

for i1 in range(Z.shape[0]):
    for i2 in range(Z.shape[1]):
        w0 = X[i1,i2]
        w1 = Y[i1,i2]

        error = lasso_error(w0=w0, w1=w1, x_true=x, y_true=y, alpha=1.0)
        Z[i1,i2] = error


#fig, (ax1, ax2) = plt.subplots(ncols=2)
#ax1.scatter(x=x, y=y)
#ax1.legend()

# https://matplotlib.org/stable/gallery/mplot3d/surface3d.html
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# create light source object.
ls = LightSource()
rgb = ls.shade(Z, plt.cm.RdYlBu)

surf = ax.plot_surface(X, Y, Z, rcount=500, ccount=500, linewidth=0, facecolors=rgb, antialiased=False, shade=True, lightsource=ls) #viridis
#ax.scatter(0,1,lasso_error(10,0,x,y,alpha=1.0), c='green')
ax.set_xlabel('intercept w0')
ax.set_ylabel('slope w1')
ax.set_zlabel('error')

ax.set_zlim(-1, 5000)
#fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()
