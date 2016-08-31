function [J, grad] = costFunctionReg(theta, X, y, lambda)
%COSTFUNCTIONREG Compute cost and gradient for logistic regression with regularization
%   J = COSTFUNCTIONREG(theta, X, y, lambda) computes the cost of using
%   theta as the parameter for regularized logistic regression and the
%   gradient of the cost w.r.t. to the parameters. 

% Initialize some useful values
m = length(y); % number of training examples

% You need to return the following variables correctly 
J = 0;
grad = zeros(size(theta));

% ====================== YOUR CODE HERE ======================
% Instructions: Compute the cost of a particular choice of theta.
%               You should set J to the cost.
%               Compute the partial derivatives and set grad to the partial
%               derivatives of the cost w.r.t. each parameter in theta

%%%%%
% version 1: no depends
%%%%%

% predictions = sigmoid(X*theta);
% J = (1/m) * sum(-y .* log(predictions) - (1-y) .* log(1-predictions)) + lambda/(2*m) * sum(theta(2:length(theta)).^2); % don't include first element of theta in sum
% grad_nonorm = (1/m) * sum((predictions - y) .* X, dim=1)';
% grad_norm_factor = lambda/m .* theta(2:length(theta),:);
% grad_norm_factor = [0; grad_norm_factor];
% grad = grad_nonorm + grad_norm_factor;

%%%%% 
% version 2: use previous cost function output
%%%%%
[J, grad] = costFunction(theta, X, y);

J_reg = lambda/(2*m) * sum(theta(2:length(theta)).^2);
J = J + J_reg;

grad_reg = [0; lambda/m .* theta(2:length(theta))];
grad = grad + grad_reg;

% =============================================================

end
