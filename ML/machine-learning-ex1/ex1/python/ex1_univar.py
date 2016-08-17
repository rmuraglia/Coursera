#! /usr/bin/env python

"""
ex1_univar.py

Python implementation of coding exercise 1 for Andrew Ng's coursera machine learning class (Week 2 assignment)
"""

import numpy as np 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

"""
Part 1: Warm up exercise - create identity matrix
"""

np.identity(5)

"""
Part 2: Plotting - create scatter plot of data
"""

# load data
dat1 = np.loadtxt('../ex1data1.txt', delimiter=',')
X = dat1[:, 0]
y = dat1[:, 1]
m = y.size

# plot data
plt.plot(X, y, marker='x', color='red', linestyle='none', markersize=10) # or plt.scatter()
plt.xlabel('Population of City in 10,000s')
plt.ylabel('Profit in $10,000s')
plt.show()

"""
Part 3: Gradient descent
"""

# initialize data for fitting
X = np.column_stack((np.ones(m), X))
theta = np.zeros(2)

def computeCost(X, y, theta) :
    J = 1.0/(2*m) * sum((np.dot(X, theta)-y)**2)
    return J

# check initial cost function value
J_init = computeCost(X, y, theta)

# set gradient descent settings
iterations = 1500
alpha = 0.01

# run gradient descent for 'iterations' number of steps
def gradient_descent(X, y, theta, alpha, num_iters) :
    J_hist = np.zeros(num_iters)

    for iter in range(num_iters) :
        theta = theta - alpha * (1.0/m) * np.sum((np.dot(X, theta) - y) * X.T, axis=1)
        J_hist[iter] = computeCost(X, y, theta)

    return theta, J_hist

theta, J_hist = gradient_descent(X, y, theta, alpha, iterations)

# plot linear fit with data
plt.plot(X[:,1], y, marker='x', color='red', linestyle='none', markersize=10, label='Training data') # or plt.scatter()
plt.xlabel('Population of City in 10,000s')
plt.ylabel('Profit in $10,000s')
plt.plot()
plt.plot(X[:,1], np.dot(X, theta), label='Linear regression')
plt.legend(numpoints=1, loc='upper right')
plt.show()

# predict values for population sizes of 35k and 70k
predict1 = np.dot([1, 3.5], theta)*10000
predict2 = np.dot([1, 7], theta)*10000

"""
Part 4: Visualizing J(theta_0, theta_1)
"""

# compute J values over grid
J_vals = np.empty([100, 100])
theta0_vals = np.linspace(-10, 10, 100)
theta1_vals = np.linspace(-1, 4, 100)

for i in range(len(theta0_vals)) :
    for j in range(len(theta1_vals)) :
        t = [theta0_vals[i], theta1_vals[j]]
        J_vals[i, j] = computeCost(X, y, t)

t0, t1 = np.meshgrid(theta0_vals, theta1_vals)

# show surface plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(t0, t1, J_vals.T, cmap='jet')
ax.set_xlabel(r'$\theta_0$')
ax.set_ylabel(r'$\theta_1$')
plt.show()

# show contour plot
plt.contour(t0, t1, J_vals.T, np.logspace(-2, 3, 20))
plt.xlabel(r'$\theta_0$')
plt.ylabel(r'$\theta_1$')
plt.plot(theta[0], theta[1], 'rx')
plt.show()
