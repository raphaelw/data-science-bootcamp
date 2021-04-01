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
    error = mse(y_true,y_pred) #+ alpha*( abs(w0)+abs(w1) )
    return error

#-------------------------------------------------

x     = np.random.randn(150)
noise = np.random.randn(150) * 0.4

y = 25.0*x + noise

limit = 50
snum = 100
all_w0 = np.linspace(start=-limit, stop=limit, num=snum)
all_w1 = np.linspace(start=-limit, stop=limit, num=snum)
all_w0, all_w1 = np.meshgrid(all_w0, all_w1)
all_errors = np.zeros_like(all_w0) # Z

for i1 in range(all_errors.shape[0]):
    for i2 in range(all_errors.shape[1]):
        w0 = all_w0[i1,i2]
        w1 = all_w1[i1,i2]

        error = lasso_error(w0=w0, w1=w1, x_true=x, y_true=y, alpha=1.0)
        all_errors[i1,i2] = error


#fig, (ax1, ax2) = plt.subplots(ncols=2)
#ax1.scatter(x=x, y=y)
#ax1.legend()

# https://matplotlib.org/stable/gallery/mplot3d/surface3d.html
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# create light source object.
ls = LightSource()
rgb = ls.shade(all_errors, plt.cm.RdYlBu)

surf = ax.plot_surface(all_w0, all_w1, all_errors, rcount=500, ccount=500, linewidth=0, facecolors=rgb, antialiased=False, shade=True, lightsource=ls) #viridis
#ax.scatter(0,1,lasso_error(10,0,x,y,alpha=1.0), c='green')
ax.set_xlabel('intercept w0')
ax.set_ylabel('slope w1')
ax.set_zlabel('error')

ax.set_zlim(-1, 5000)
#fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()
