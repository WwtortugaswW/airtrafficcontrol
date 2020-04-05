"""
@package src 
@author andresgonzalezfornell

Generator of the air traffic chart in the user interface.
"""

from src.core import spherical2Cartesian  #TODO: change core
from math import pi  #TODO: delete


class Chart:
    """Generator of the air traffic chart in the user interface."""
    ##@var app
    #appJar GUI object
    app = None
    ##@var legend
    #Legend of element colors
    legend = {"commercial" : "Blue", "military" : "Red"}
    ##@var scale
    #Chart scale vector [x, y] in meters/pixels
    scale = [6.3781E6 * pi / 180, 6.3781E6 * pi / 180]  #TODO: change scale from GUI
    ##@var focus
    #Chart position coordinates [longitude, latitude] in degrees of the top left corner  
    focus = [0.0, 0.0]  #TODO: change focus from GUI
    ##@var __height
    #Canvas GUI size [width, height] in pixels
    __size = [600, 600]
    ##@var __width
    ##@var __diameter
    #Element GUI diameter in pixels
    __diameter = 10
    
    def __init__(self, app, row=0, column=0):
        """Class constructor.
            @param app       appJar GUI object
            @param row       row position in the user interface
            @param column    column position in the user interface
        """
        self.app = app
        if self.app:
            self.app.addCanvas("chart", row=row, column=column)
            self.app.setCanvasWidth("chart", self.__size[0])
            self.app.setCanvasHeight("chart", self.__size[1])
    
    def clear(self):
        """It clears the chart."""
        if self.app:
            self.app.clearCanvas("chart")
        
    def add(self, element):
        """It adds an element to the chart.
            @param element    element
        """
        if self.app is not None:
            if element.__class__.__name__ == "Airport":
                #Spherical coordinates [longitude, latitude] in degrees
                spherical = element.location
                #Cartesian coordinates [x, y] in meters
                coordinates = spherical2Cartesian(element.location, self.focus)
                #Position in pixels
                position = [coordinates[0] / self.scale[0], coordinates[1] / self.scale[1]]
                self.app.addCanvasRectangle("chart", position[0], position[1], self.__diameter, self.__diameter, fill=self.legend[element.industry])
            elif element.__class__.__name__ == "Airplane":
                #Spherical coordinates [longitude, latitude] in degrees
                if element.location.__class__.__name__ == "Airport":
                    spherical = element.location.location
                else:
                    spherical = element.location
                #Cartesian coordinates [x, y] in meters
                coordinates = spherical2Cartesian(spherical, self.focus)
                #Position in pixels
                position = [coordinates[0] / self.scale[0], coordinates[1] / self.scale[1]]
                self.app.addCanvasCircle("chart", position[0], position[1], self.__diameter, fill=self.legend[element.industry])
            elif (element.__class__.__name__ == "Flight"):
                #Spherical coordinates [longitude, latitude] in degrees
                spherical = [element.origin.location, element.destination.location]
                #Cartesian coordinates [[x_origin, y_origin][x_destination, y_destination]] in meters
                coordinates = [spherical2Cartesian(spherical[0], self.focus),
                               spherical2Cartesian(spherical[1], self.focus)]
                #Position in pixels
                position = [[coordinates[0][0] / self.scale[0], coordinates[0][1] / self.scale[1]],
                            [coordinates[1][0] / self.scale[0], coordinates[1][1] / self.scale[1]]]
                self.app.addCanvasLine("chart", position[0][0], position[0][1], position[1][0], position[1][1])
