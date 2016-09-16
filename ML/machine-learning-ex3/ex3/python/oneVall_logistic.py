#! /usr/bin/env python

"""
oneVall_logistic.py
Python implementation of part 1 of coding exercise 3 for Andrew Ng's coursera machine learning class (week 4 assignment)
Part 1 trains a one versus all logistic regression classifier
From now until remainder of course, will be doing manual implementations in Octave to help learn the nitty-gritty of algorithms, but then will be deferring to python libraries for python implementations to learn more practical experience.
"""

import scipy.io as sio
from sklearn import linear_model

# load data from MATLAB file
mat_contents = sio.loadmat('../ex3data1.mat')
X = mat_contents['X']
y = mat_contents['y'].ravel()

lam = 0.1 # set shrinkage param

# fit model
lr = linear_model.LogisticRegression(C=1/lam, multi_class='ovr', fit_intercept=True)
lr.fit(X, y)

# access fit params
# lr.coef_ # for the feature thetas
# lr.intercept_ # for the dummy variable (all ones) intercept thetas

# predict labels
predictions = lr.predict(X)

# calculate accuracy on these predictions
pred_accuracy = lr.score(X, y)
