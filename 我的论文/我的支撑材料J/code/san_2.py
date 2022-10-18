import sympy
import numpy as np

r = sympy.symbols('r')
a = sympy.symbols('a')
x0, y0 =sympy.symbols('x0 y0')
x1, y1 = sympy.symbols('x1 y1') 
x2, y2 = sympy.symbols('x2 y2') 
x3, y3 = sympy.symbols('x3 y3') 
x01, x12, x13 = sympy.symbols('x01 x12 x13') 
k12, k10, k_ = sympy.symbols('k12 k10 k_') 
s02, p02, s10, p10 = sympy.symbols('s02 p02 s10 p10') 
x0, y0 = 0, 0
x1, y1 = 100, 0 
x2, y2 = 76.6044, 64.2788
# x3, y3 = 17.3648, 98.4808
r = sympy.sqrt((x0 - x1)**2 + (y0 - y1)**2)

k10 = x1**2 + y1**2 - 2 * (x1 * x0 + y1 * y0)
k12 = x1**2 + y1**2 - 2 * (x2 * x1 + y2 * y1)
k_ = 2 * r * sympy.sin(a) - (x1**2 + y1**2)

s02 = x0 - x2
s10 = x1 - x2
p02 = y0 + y2 
p10 = y1 + y0

y3 = ((s10 * (k12 - k10) - s02 * (k12 - k_))/2) / (p02 * s10 - p10 * s02)
x3 = (((k12 - k10) / 2) - y3 * p10) / s02

print("x3:",x3)
print("====")
print("y3:",y3)