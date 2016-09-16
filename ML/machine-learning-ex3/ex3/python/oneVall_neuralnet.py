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
Theta1 = mat_contents2['Theta1']
Theta2 = mat_contents2['Theta2']
features_theta1 = Theta1.T[1:input_layer_size+1, :]
intercept_theta1 = Theta1.T[0, :]
features_theta2 = Theta2.T[1:hidden_layer_size+1, :]
intercept_theta2 = Theta2.T[0, :]

"""
method 1: with sklearn library
"""

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

"""
method 2: actually using the forward propagation algorithm
"""

num_examples = X.shape[0]
num_labels = Theta2.shape[0]

# goal: return a vector of length num_examples with best guess labels of each example

def sigmoid(z) :
    g = 1.0/(1+np.exp(-z))
    return g

# add ones to X
X = np.column_stack((np.ones(num_examples), X))

# calculate hidden layer sigmoid output
a_1 = sigmoid(np.dot(X, Theta1.T))

# add ones to hidden layer
a_1 = np.column_stack((np.ones(num_examples), a_1))

# get output node values
a_2 = sigmoid(np.dot(a_1, Theta2.T))

# get indices of best classification probability for each row
best_ind = np.argmax(a_2, axis=1)

# return actual labels
labels_pred = (np.arange(10) + 1)[best_ind]

# score accuracy
np.mean(labels_pred==y)



