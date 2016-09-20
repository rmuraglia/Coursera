function [C, sigma] = dataset3Params(X, y, Xval, yval)
%EX6PARAMS returns your choice of C and sigma for Part 3 of the exercise
%where you select the optimal (C, sigma) learning parameters to use for SVM
%with RBF kernel
%   [C, sigma] = EX6PARAMS(X, y, Xval, yval) returns your choice of C and 
%   sigma. You should complete this function to return the optimal C and 
%   sigma based on a cross-validation set.
%

% You need to return the following variables correctly.
C = 1;
sigma = 0.3;

% ====================== YOUR CODE HERE ======================
% Instructions: Fill in this function to return the optimal C and sigma
%               learning parameters found using the cross validation set.
%               You can use svmPredict to predict the labels on the cross
%               validation set. For example, 
%                   predictions = svmPredict(model, Xval);
%               will return the predictions on the cross validation set.
%
%  Note: You can compute the prediction error using 
%        mean(double(predictions ~= yval))
%
C_vec = [0.01 0.03 0.1 0.3 1 3 10 30];
% C_vec = [0.01 0.03 0.1]; % truncated testing set
s_vec = C_vec;
pred_err = Inf;

for C = C_vec
    for sigma = s_vec
        fprintf(['Testing parameters: C=%f and sigma=%f ...\n'], C, sigma);
        model = svmTrain(X, y, C, @(x1, x2) gaussianKernel(x1, x2, sigma));
        predictions = svmPredict(model, Xval);
        pred_err_temp = mean(double(predictions ~= yval));
        if (pred_err_temp < pred_err)
            pred_err = pred_err_temp;
            C_out = C;
            sigma_out = sigma;
        end
    end
end

C = C_out;
sigma = sigma_out;

% =========================================================================

end
