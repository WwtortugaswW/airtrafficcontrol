'''
Created on 4 abr. 2020

@author: administrador
'''
from math import sqrt
from src.spherical import conversor
from src import spherical


class Flight:
    ident = None  # número de vuelo
    created = None  # fecha de creación
    airplane = None  # avión del vuelo
    origin = None  # aeropuerto de salida
    destination = None  # aeropuerto de llegada
    time = 0
    flying= False

    def __init__(self, flight):
        for atrib in flight:
            setattr(self, atrib, flight[atrib])
       
    def start(self):
        """It starts the flight."""
        self.flying = True
  
    def stop(self):
        """It stops the flight."""
        self.flying = False
    
    def getTripVector(self):
        """It returns the unitary vector which points the trip direction."""
        distance = [None] * min(len(self.origin.location), len(self.destination.location))  # FIXME: TypeError: object of type 'Airport' has no len()
        cartesiandestinationlocation=conversor(self.destination.location)
        cartesianoriginlocation=conversor(self.origin.location)
        for n in range(0, len(distance)):
            distance[n] = cartesiandestinationlocation[n] - cartesianoriginlocation[n]
        
        return distance
    
    def getCurrentDistance(self):
        """It returns the traveled distance of the flight in seconds.
        """
        return self.airplane.speed * self.time
                            
    def elapse(self, time):  # FIXME: poner un if que diga si está start en funcionamiento hacer eso, sino nada
        """It updates the flight according to a given elapsed time. 
            @param time    time increase since the last update
        """
        if self.flying & self.getCurrentDistance() < self.calculateDistance():
            self.time += time
            v = [None] * len(self.getTripVector())
            for n in range (0, len(v)):
                v[n] = (self.getTripVector()[n] / self.calculateDistance()) * self.airplane.speed
            for n in range (0, len(v)):
                self.airplane.location[n] += v[n] * time
        elif self.flying & self.getCurrentDistance() >= self.calculateDistance():
            self.airplane.location = self.destination.location
        
# FIXME: Si no se borran los vuelos, el numero de aviones al borrarlo no disminuye

    def calculateDistance(self):
        """It returns the total distance of the flight in meters."""
        distance = self.getTripVector()
        sumapower = 0
        for dimension in range(0, len(distance)):
            sumapower += distance[dimension] ** 2
        distance = sqrt(sumapower)
        return distance
        
    def calculateCurrentTime (self):
        """It returns the traveled time of the flight in seconds."""
        return self.time
    
    def calculateTime(self):
        """It returns the total time of the flight in seconds."""
        return self.calculateDistance() / self.airplane.speed
    
    def calculateETA(self):
        """It returns the remaining time to arrive in seconds."""
        return self.calculateTime() - self.calculateCurrentTime()
