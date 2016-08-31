#! /usr/bin/env python

"""
logistic_regression.py

Python implementation of coding exercise 2 for Andrew Ng's coursera machine learning class (week 3 assignment)
"""

import numpy as np 
import matplotlib.pyplot as plt
import scipy.optimize as optimize

"""
Part 1: Visualize the data
"""

# load data
dat1 = np.loadtxt('../ex2data1.txt', delimiter=',')
X = dat1[:, 0:2]
y = dat1[:, 2]

# get indices of admitted and not admitted groups
indT = np.where(y==1)[0] # where returns a tuple, for which we only want to first entry
indF = np.where(y==0)[0] # second entry in tuple is just empty anyway

# scatter plot: colors and shapes by admit status
fig, ax = plt.subplots()
ax.plot(X[indT, 0], X[indT, 1], marker='+', markeredgecolor='black', linestyle='none', label='Admitted')
ax.plot(X[indF, 0], X[indF, 1], marker='o', markerfacecolor='yellow', linestyle='none', label='Not admitted')
ax.legend(numpoints=1, loc='upper right')
ax.set_xlabel('Exam 1 score')
ax.set_ylabel('Exam 2 score')
fig.show()

"""
Part 2: Sigmoid function
"""

def sigmoid(z) :
    g = 1.0/(1+np.exp(-z))
    return g

# print sigmoid(0), sigmoid(10), sigmoid(-10)

"""
Part 3: Cost function and gradient
"""

def costFunction(theta, X, y) :
    m = len(y)
    predictions = sigmoid(np.dot(X, theta))
    J = (1.0/m) * sum(-y * np.log(predictions) - (1-y) * np.log(1-predictions))
    grad = (1.0/m) * np.sum((predictions - y) * X.T, axis=1)
    return J, grad

# initialize data for fitting
X = np.column_stack((np.ones(X.shape[0]), X))
init_theta = np.zeros(X.shape[1])

init_cost = costFunction(init_theta, X, y)[0]

"""
Part 4: Optimization using scipy routine
"""

def costTheta(theta) :
    m = len(y)
    predictions = sigmoid(np.dot(X, theta))
    J = (1.0/m) * sum(-y * np.log(predictions) - (1-y) * np.log(1-predictions))
    return J

def gradTheta(theta) :
    m = len(y)
    predictions = sigmoid(np.dot(X, theta))
    grad = (1.0/m) * np.sum((predictions - y) * X.T, axis=1)
    return grad

res = optimize.minimize(costTheta, init_theta, method='TNC', jac=gradTheta, options={'disp': True}) # could have also used Nelder-Mead, or other method options. just BFGS appears to throw an error...
opt_theta = res.x

print 'Optimal theta found', opt_theta
print 'Cost at optimal theta', res.fun

"""
Part 5: Plot decision boundary
"""

# decision boundary will be linear - get exam 1 score plotting end points
plot_x = np.array([min(X[:, 1])-2, max(X[:, 1])+2])

def boundary_y_from_x(x, theta) :
    # decision boundary is where theta.T * X = theta_0 + theta_1*x_1 + theta_2*x_2 = 0
    # solve for x_2 given theta and x_1
    y = (theta[0] + theta[1]*x) / (-theta[2])
    return y

plot_y = boundary_y_from_x(plot_x, opt_theta)

fig, ax = plt.subplots()
ax.plot(X[indT, 1], X[indT, 2], marker='+', markeredgecolor='black', linestyle='none', label='Admitted')
ax.plot(X[indF, 1], X[indF, 2], marker='o', markerfacecolor='yellow', linestyle='none', label='Not admitted')
ax.plot(plot_x, plot_y, color='blue', label='Decision Boundary')
ax.legend(numpoints=1, loc='upper right')
ax.set_xlabel('Exam 1 score')
ax.set_ylabel('Exam 2 score')
fig.show()

"""
Part 6: Prediction and accuracy
"""

# predict acceptance probability for student with scores of 45 and 85
prob = sigmoid(np.dot(np.array([1, 45, 85]), opt_theta))

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



