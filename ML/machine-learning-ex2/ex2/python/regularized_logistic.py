#! /usr/bin/env python

"""
regularized_logistic.py

Python implementation of part 2 of coding exercise 2 for Andrew Ng's coursera machine learning class (week 3 assignment)
"""

import numpy as np 
import matplotlib.pyplot as plt 
import scipy.optimize as optimize

"""
Part 1: visualize the data
"""

# load data
dat2 = np.loadtxt('../ex2data2.txt', delimiter=',')
X = dat2[:, 0:2]
y = dat2[:, 2]

# get group indices
indT = np.where(y==1)[0]
indF = np.where(y==0)[0]

# scatter plot by accept/reject status
fig, ax = plt.subplots()
ax.plot(X[indT, 0], X[indT, 1], marker='+', markeredgecolor='black', linestyle='none', label='Accepted')
ax.plot(X[indF, 0], X[indF, 1], marker='o', markerfacecolor='yellow', linestyle='none', label='Rejected')
ax.legend(numpoints=1, loc='upper right')
ax.set_xlabel('Microchip Test 1')
ax.set_ylabel('Microchip Test 2')
fig.show()

"""
Part 2: Add polynomial expansion features and compute initial conditions
"""

def mapFeature(X, max_degree) :
    # make all power combinations up to max_degree

    # initialize with 0 exponent - just ones
    if len(X.shape) == 1 :
        features_out = np.ones(1)
    else :
        features_out = np.ones(X.shape[0]) 

    for i in np.linspace(1, max_degree, max_degree) :
        for j in np.linspace(0, i, i+1) :
            # print i-j, j
            try :
                new_feature = (X[:,0]**(i-j) * X[:,1]**j)
                features_out = np.column_stack((features_out, new_feature))
            except IndexError :
                new_feature = (X[0]**(i-j) * X[1]**j)
                features_out = np.append(features_out, new_feature)
    return features_out

max_degree = 6
X = mapFeature(X, max_degree)
init_theta = np.zeros(X.shape[1])
lam = 1.0

def sigmoid(z) :
    g = 1.0/(1+np.exp(-z))
    return g

def costFuncReg(theta, X, y) :
    m = len(y)
    predictions = sigmoid(np.dot(X, theta))
    J = (1.0/m) * sum(-y * np.log(predictions) - (1-y) * np.log(1-predictions))
    J_reg = lam/(2*m) * sum(theta[1:len(theta)]**2)
    J = J + J_reg
    grad = (1.0/m) * np.sum((predictions -y) * X.T, axis=1)
    grad_reg = np.append(0, lam/m * theta[1:len(theta)])
    grad = grad + grad_reg
    return J, grad

init_J, init_grad = costFuncReg(init_theta, X, y)

"""
Part 3: Optimize theta
"""

def Jreg(theta) :
    m = len(y)
    predictions = sigmoid(np.dot(X, theta))
    J = (1.0/m) * sum(-y * np.log(predictions) - (1-y) * np.log(1-predictions))
    J_reg = lam/(2*m) * sum(theta[1:len(theta)]**2)
    J = J + J_reg
    return J

def gradreg(theta) :
    m = len(y)
    predictions = sigmoid(np.dot(X, theta))
    grad = (1.0/m) * np.sum((predictions -y) * X.T, axis=1)
    grad_reg = np.append(0, lam/m * theta[1:len(theta)])
    grad = grad + grad_reg
    return grad

res = optimize.minimize(Jreg, init_theta, method='BFGS', jac=gradreg, options={'disp': True})
opt_theta = res.x

"""
Part 4: plot boundary and compute training accuracy
"""

# define a plotting area
u = np.linspace(-1, 1.5, 50)
v = np.linspace(-1, 1.5, 50)

# compute theta.T * X over all points in the grid
z = np.zeros((len(u), len(v)))
for i in xrange(len(u)) :
    for j in xrange(len(v)) :
        z[i,j] = np.dot(mapFeature(np.array((u[i], v[j])), max_degree), opt_theta)

# plot contour with only 0-level shown (corresponds to decision boundary)
fig, ax = plt.subplots()
ax.contour(v, u, z, levels=[0], colors='green', label='Decision boundary') # for contour, either transpose z, or put v as rows and u as columns
ax.plot(X[indT, 1], X[indT, 2], marker='+', markeredgecolor='black', linestyle='none', label='Accepted')
ax.plot(X[indF, 1], X[indF, 2], marker='o', markerfacecolor='yellow', linestyle='none', label='Rejected')
ax.legend(numpoints=1, loc='upper right')
ax.set_xlabel('Microchip Test 1')
ax.set_ylabel('Microchip Test 2')
fig.show()

# compute training set accuracy
def predict(theta, X) :
    # return a vector p of 0/1 classifications
    p = np.zeros(X.shape[0])
    predictions = sigmoid(np.dot(X, theta))
    pred0 = np.where(predictions<0.5)[0]
    pred1 = np.where(predictions>=0.5)[0]
    p[pred0] = 0
    p[pred1] = 1
    return p 

p = predict(opt_theta, X)

print 'Our accuracy on the training set was', np.mean(p==y)*100, '%'

