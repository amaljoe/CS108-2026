'''
    Geometry (Complex and Polar)
    Author: Saksham Rathi
'''
import math
from complex import Complex
from polar import Polar


def modulus(c: Complex):
    '''return modulus of the complex number'''
    return round(math.sqrt(c.x**2 + c.y**2), 2)


def arg(c: Complex):
    '''return arg (angle) of the complex number'''
    return round(math.atan2(c.y, c.x), 2)


def abscissa(p: Polar):
    '''return abscissa of the polar point'''
    return round(p.r * math.cos(p.t), 2)


def ordinate(p: Polar):
    '''return ordinate of the polar point'''
    return round(p.r * math.sin(p.t), 2)


def distance(z1: Complex, z2: Complex):
    '''distance between points'''
    return modulus(z1 - z2)


if __name__ == '__main__':
    a = Complex(1, 2)
    b = Complex(2, 2)
    z = a + b
    print(z)
    x = Polar(2, math.pi/3)
    print(x ** 2)
