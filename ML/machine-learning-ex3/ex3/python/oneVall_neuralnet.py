"""
oneVall_neuralnet.py
Python implementation of part 2 of coding exercise 3 for Andrew Ng's coursera machine learning class (week 4 assignment)
Part 2 calculates the training set accuracy of this neural net for a provided set of weights
"""

import numpy as np
import scipy.io as sio
from sklearn import neural_network

# load feature and label data
# loadmat makes a dictionary, so check the available variable names with mat_contents.keys()
input_layer_size = 400
hidden_layer_size = 25
num_labels = 10

mat_contents = sio.loadmat('../ex3data1.mat')
X = mat_contents['X']
y = mat_contents['y'].ravel()

# load precomputed weights
mat_contents2 = sio.loadmat('../ex3weights.mat')
Theta1 = mat_contents2['Theta1'].T
Theta2 = mat_contents2['Theta2'].T
features_theta1 = Theta1[1:input_layer_size+1, :]
intercept_theta1 = Theta1[0, :]
features_theta2 = Theta2[1:hidden_layer_size+1, :]
intercept_theta2 = Theta2[0, :]

# initialize neural net
nn = neural_network.MLPClassifier(hidden_layer_sizes=(hidden_layer_size,), activation='logistic')

# give neural net the precomputed info (and everything else it needs)
nn.fit(X, y) # fit a model
nn.coeffs_ = [features_theta1, features_theta2] # overwrite with provided params
nn.intercepts_ = [intercept_theta1, intercept_theta2]

# predict
predictions = nn.predict(X)

# score
pred_accuracy = nn.score(X, y)
