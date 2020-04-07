'''
Created on 4 abr. 2020

@author: administrador
'''

from enum import Enum


class Object:
    ident = None  # Atributos del objeto (ISO o Matrícula)
    created = None  # fecha de creación
    location = None  # Coordenadas
    industry = None

    def __init__(self, objecto):
        for atrib in objecto:
            setattr(self, atrib, objecto[atrib])
    
    class Industry(Enum):  # tipo de avión
        military = "military"
        commercial = "commercial"
        passenger = "passenger"
        
        @staticmethod
        def options():
            return ["military", "commercial", "passenger"]


class Airport(Object):
    pass


class Airplane(Object):
    manufacturer = None  # fabricante
    model = None  # modelo
    speed = None  # velocidad media
    
    def __init__(self, objecto):
        Object.__init__(self, objecto)
        if isinstance(self.location, Airport):
            self.location = self.location.location


class Prueba(Object):
    pass

    def __init__(self, arg):
        print("argumento = " + arg)
