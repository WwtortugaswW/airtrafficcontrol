'''
Created on 4 abr. 2020

@author: administrador
'''
from math import pi
Rt = 6.3781E6  # Radio de la Tierra (m)


def conversor (spherical, offset=[0,0]):
    cartesian = [None]*len(spherical)
    for dimension in range(0, len(spherical)):
        cartesian[dimension] = (spherical[dimension]-offset[dimension]) * 2 * pi / 360 * Rt
    return cartesian