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
w0 = 0.0 # intercept
w1 = 25.0 # slope
num_samples = 150
x = np.random.randn(num_samples)
noise = np.random.randn(num_samples) * 0.3*w1
y_ideal = model(w0=w0, w1=w1, x=x)
y = y_ideal + noise

# plot
fig = plt.figure(constrained_layout=False, figsize=(10,5))
grid_spec = fig.add_gridspec(ncols=2, nrows=1)
ax1 = fig.add_subplot(grid_spec[0])
ax2 = fig.add_subplot(grid_spec[1], projection='3d')

# 2D ---------------
ax1.scatter(x=x, y=y, label='Data', alpha=0.5)
ax1.plot(x, y_ideal, color='k', label=f'Ideal fit ($w_0={w0}$; $w_1={w1}$)')
ax1.legend()
ax1.set_xlabel('x')
ax1.set_ylabel('y')

# 3D ---------------
# https://matplotlib.org/stable/gallery/mplot3d/surface3d.html

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

# create light source object
ls = LightSource()
rgb = ls.shade(Z, plt.cm.RdYlBu)

surf = ax2.plot_surface(X, Y, Z, rcount=500, ccount=500, linewidth=0, facecolors=rgb, antialiased=False, shade=True, lightsource=ls)
ax2.set_xlabel('intercept $w_0$')
ax2.set_ylabel('slope $w_1$')
ax2.set_zlabel('error')

ax2.set_zlim(-1, 6000)

# https://matplotlib.org/stable/gallery/mplot3d/rotate_axes3d_sgskip.html
#ax2.view_init(10, 40) 
#ax2.view_init(38, 160)
ax2.view_init(10, 12)

#fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()
