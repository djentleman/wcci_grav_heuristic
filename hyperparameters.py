# contains all hyperparameters

granularity = 500 # grid search + visualization granulatory
# eg 500 = 500 x 500 pixels, 500^2 ops
lxb = -10; uxb = 10; # function x bounds
lyb = -10; uyb = 10; # function y bounds
dT = 1 # delta time
cor = 0.2 # Coefficient of restitution, needs to be less than 1
delay = 0 # delay between iterations
ui = True # render ui?