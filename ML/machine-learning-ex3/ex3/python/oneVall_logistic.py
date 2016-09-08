#! /usr/bin/env python

"""
oneVall_logistic.py
Python implementation of part 1 of coding exercise 3 for Andrew Ng's coursera machine learning class (week 4 assignment)
Part 1 trains a one versus all logistic regression classifier
"""

import numpy as np 
import scipy.optimize as op
import scipy.io as sio

# load data from MATLAB file
mat_contents = sio.loadmat('../ex3data1.mat')
X = mat_contents['X']
y = mat_contents['y']

# ran into issues with minimization - possibly because of zero gradient for some dimensions?
# further inspection shows that some features are ALL zero - let's prune out features that have no variance
X_full = X
feature_vars = np.var(X_full, axis=0) # get each column (feature) variance
X = np.compress(feature_vars!=0, X, axis=1) # extract non zero var columns

# equiv method from index values instead of bool:
# good_features = np.where(feature_vars!=0)[0]
# X = np.take(X_full, good_features, axis=1)

# set useful params
input_layer_size = X.shape[1] # 20x20 images for 400 pixels as features
num_labels = len(np.unique(y)) # 10 possible labels. note: 0 label written as 10 for 1-indexed octave.
m = X.shape[0] # number of training examples
lam = 0.1 # shrinkage param

def oneVsAll(X, y, num_labels, lam) :
    # train a logistic regression classifier for each label
    # return a matrix, where each row are the coefficients for the i-th label

    (m, n) = X.shape

    all_theta = np.empty((num_labels, n+1))
    X = np.column_stack((np.ones(X.shape[0]), X))

    for i in xrange(num_labels) :
        init_theta = np.zeros(n+1)
        y_bool = y==(i+1)
        # res = op.minimize(Jfunc, init_theta, args=(X, y_bool, lam), method='BFGS', jac=Gfunc, options={'disp': True})
        res = op.minimize(Jfunc, init_theta, args=(X, y_bool, lam), method='Nelder-Mead', options={'disp': True})
        opt_theta = res.x
        all_theta[i,:] = opt_theta

    return all_theta

def logistic_h(theta, X) :
    # get hypothesis function for logistic regression (prediction probability)
    z = np.dot(X, theta)
    g = 1.0/(1+np.exp(-z))
    return g[:, np.newaxis]

def Jfunc(theta, X, y_bool, lam) :
    m = len(y_bool)
    predictions = logistic_h(theta, X)
    J_unreg = (1.0/m) * sum(-y_bool * np.log(predictions) - (1-y_bool) * np.log(1-predictions))
    J = J_unreg + lam/(2*m) * sum(theta[1:len(theta)]**2)
    return J[0]

def Gfunc(theta, X, y_bool, lam) :
    m = len(y_bool)
    predictions = logistic_h(theta, X)
    grad_unreg = (1.0/m) * np.sum((predictions - y_bool) * X, axis=0)
    grad = grad_unreg + np.append(0, lam/m * theta[1:len(theta)])
    return grad
