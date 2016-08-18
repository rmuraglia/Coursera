#! /usr/bin/env python

"""
ex1_multivar.py

Python implementation of optional portion of coding exercise 1 for Andrew Ng's coursera machine learning class (week 2 assignment)
"""

import numpy as np 
import matplotlib.pyplot as plt 

"""
Part 1: Feature normalization
"""

# load data
dat2 = np.loadtxt('../ex1data2.txt', delimiter=',')
X = dat2[:, 0:2]
y = dat2[:, 2]
m = len(y)

# scale and center features
def featureNormalize(X) :
    X_norm = np.empty(X.shape)
    mu = np.mean(X, axis=0)
    sigma = np.std(X, axis=0)

    X_norm = (X - mu) / sigma
    return X_norm, mu, sigma

X, mu, sigma = featureNormalize(X)

# add intercept term to X
X = np.column_stack((np.ones(m), X))

"""
Part 2: Gradient descent
"""

# set params and run gradient descent
alpha = 0.01
num_iters = 400
theta = np.zeros(X.shape[1])

def computeCost(X, y, theta) :
    J = 1.0/(2*m) * sum((np.dot(X, theta)-y)**2)
    return J

def gradient_descent(X, y, theta, alpha, num_iters) :
    J_hist = np.zeros(num_iters)

    for iter in range(num_iters) :
        theta = theta - alpha * (1.0/m) * np.sum((np.dot(X, theta)-y)[:,np.newaxis] * X, axis=0)
        J_hist[iter] = computeCost(X, y, theta)

    return theta, J_hist

theta, J_hist = gradient_descent(X, y, theta, alpha, num_iters)

# plot convergence monitoring graph
plt.plot(range(num_iters), J_hist)
plt.xlabel('Number of iterations')
plt.ylabel('Cost J')
plt.show()

# estimate cost of 1650 sq-ft, 3 br house
test_house = [1650, 3]
thouse_norm = (test_house - mu) / sigma
thouse_norm = np.insert(thouse_norm, 0, 1) # insert a 1 in the 0th position of the vector

price = np.dot(thouse_norm, theta)

"""
Part 3: Normal equations
"""

# reload data
dat2 = np.loadtxt('../ex1data2.txt', delimiter=',')
X = dat2[:, 0:2]
y = dat2[:, 2]
m = len(y)

X = np.column_stack((np.ones(m), X))

# calculate theta by normal equation
def normalEqn(X, y) :
    theta = np.dot(np.dot(np.linalg.pinv(np.dot(X.T,X)), X.T), y)
    return theta

theta = normalEqn(X, y)

# estimate price of previous house
test_house = np.insert(np.asarray(test_house, dtype=np.float64), 0, 1)
price = np.dot(test_house, theta)

