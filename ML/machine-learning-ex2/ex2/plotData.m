function plotData(X, y)
%PLOTDATA Plots the data points X and y into a new figure 
%   PLOTDATA(x,y) plots the data points with + for the positive examples
%   and o for the negative examples. X is assumed to be a Mx2 matrix.

% Create New Figure
figure; hold on;

% ====================== YOUR CODE HERE ======================
% Instructions: Plot the positive and negative examples on a
%               2D plot, using the option 'k+' for the positive
%               examples and 'ko' for the negative examples.
%

% get indices for admit/noadmit groups
in = find(y==1);
out = find(y==0);

% plot exam score scatter, by admit status
plot(X(in, 1), X(in, 2), '+k;Admitted;');
plot(X(out, 1), X(out, 2), 'ok;Not Admitted;', 'markerfacecolor', 'yellow');
xlabel('Exam 1 score');
ylabel('Exam 2 score');

% =========================================================================

hold off;

end
