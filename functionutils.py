
from math import *

def sphere(x, y):
    return (x**2 + y**2)

def pyramid(x, y):
    return -(abs(x + y) + abs(y - x)) + 10

def ackley(x, y):
    return (-20*exp(-0.2*sqrt(0.5*(x**2 + y**2))) - exp(0.5*(cos(2*pi*x) + cos(2*pi*y))) + e + 20)

def waves(x, y):
    return 20*(sin(3*x) + sin(3*y) + 20*sin(x)) + -(-abs(x**2 + (y+3)**2) + 2) + 10*x + 100*y

def pyramidal(x, y):
    return 10*pyramid(sin(x), sin(y))-90 + 0.1*x + 0.1*y

def npyramidal(x, y):  return pyramidal(pyramidal(x, y), pyramidal(x, y))

def spherewave(x, y):
    return 10*sphere(sin(x), sin(y)) + 0.1*x + 0.1*y

def rosenbrock(x, y):
    return (100*(y - x**2)**2 + (1-x)**2)


def beale(x, y):
    return ((1.5-x+x*y)**2+(2.25-x-x*y**2)**2+(2.625-x+x*y**3)**2)

def rastagrin(x, y):
    return -20 +  (x**2 -10*cos(2*pi*x)) + (y**2 -10*cos(2*pi*y))

def scwefel(x, y):
    return  -x*sin(sqrt(abs(x)))  + -y*sin(sqrt(abs(y)))   + 2*(418.982887)

def matyas(x, y):
    return 0.26*(x**2+y**2)-0.48*(x*y)

def griewank(x, y):
    return  1 + ((x**2/4000) + (y**2/4000)) - (cos(x/sqrt(2)) * cos(y/sqrt(2)))
