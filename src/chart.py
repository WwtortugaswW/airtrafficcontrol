"""
@package src 
@author andresgonzalezfornell

Generator of the air traffic chart in the user interface.
"""


class Chart:
    """Generator of the air traffic chart in the user interface."""
    ##@var app
    #appJar GUI object
    app = None
    ##@var scale
    #Chart scale vector [x, y] in pixels/meters
    scale = [10.0, 10.0]  
    ##@var focus
    #Chart position coordinates [longitude, latitude] in degrees of the top left corner  
    focus = [0.0, 0.0]
    ##@var legend
    #Legend of element colors
    legend = {"Commercial" : "Blue", "Military" : "Red"}
    ##@var __height
    #Canvas GUI size [width, height] in pixels
    __size = [600, 600]
    ##@var __width
    ##@var __diameter
    #Element GUI diameter in pixels
    __diameter = 10
    ##@var __earthradius
    #Earth radius in meters to convert from spherical coordinates to Cartesian coordinates
    __earthradius = 1  #6.3781E6
    
    def __init__(self, app, row=0, column=0):
        """Class constructor.
            @param app       appjar GUI object
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
        self.app.clearCanvas()
        print("Chart cleared")
        
    def add(self, element):
        """It adds an element to the chart.
            @param element    element
        """
        if (element.__class__.__name__ == "Airport"):
            coordinates = [self.scale[0] * self.__spherical2Cartesian(element.location)[0],
                           self.scale[1] * self.__spherical2Cartesian(element.location)[1]]
            self.app.addCanvasRectangle("chart", coordinates[0], coordinates[1], self.__diameter, self.__diameter, fill=self.legend[element.industry])
        elif (element.__class__.__name__ == "Airplane"):
            coordinates = [self.scale[0] * self.__spherical2Cartesian(element.location)[0],
                           self.scale[1] * self.__spherical2Cartesian(element.location)[1]]
            self.app.addCanvasCircle("chart", coordinates[0], coordinates[1], self.__diameter, fill=self.legend[element.industry])
        elif (element.__class__.__name__ == "Flight"):
            coordinates = [[self.scale[0] * self.__spherical2Cartesian(element.origin)[0],
                            self.scale[1] * self.__spherical2Cartesian(element.origin)[1]],
                           [self.scale[0] * self.__spherical2Cartesian(element.destination)[0],
                            self.scale[1] * self.__spherical2Cartesian(element.destination)[1]]]
            self.app.addCanvasLine("chart", coordinates[0][0], coordinates[0][1], coordinates[1][0], coordinates[1][1])
        #TODO: selector
        
    def __spherical2Cartesian(self, spherical):
        """It converts from spherical coordinates in degrees to Cartesian coordinates in meters around the focus.
            @param spherical  spherical coordinates in degrees [longitude, latitude]
        """
        cartesian = [0, 0]
        for dimension in range(len(spherical)):
            cartesian[dimension] = self.__earthradius * (spherical[dimension] - self.focus[dimension])
        return cartesian
