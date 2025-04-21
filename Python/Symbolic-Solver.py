from sympy import * 
Rx, R3, Rdiv = symbols('x y z')
solve(Eq((Rx * R3 * Rdiv) / (Rx + R3)), Rx)