"""
@package src
@author andresgonzalezfornell

User interface.
"""

from src import chart
from datetime import datetime


class App:
    """Class of the user interface."""

    ##@var __appname
    #Name of the self.application
    __appname = "Air traffic control"
    ##@var __separator
    #Character to separate some strings for widget names
    __separator = "_"
    ##@var app
    #appJar GUI object
    app = None
    ##@var chart
    #Chart object
    chart = chart.Chart(app)
    ##@var elements
    #Sets of existing elements.
    elements = {"Airport" : {}, "Airplane" : {}, "Flight" : {}}
    ##@var info
    #Relevant info of the selected object to show on the selection panel 
    info = {"Airport": {
                "id": {"label": "Airport code", "type": "text"},
                "location": {"label":"Location", "type": "coordinates"}},
            "Airplane": {
                "id": {"label":"Plate", "type": "text"},
                "manufacturer":{"label":"Manufacturer", "type": "text"},
                "model":{"label":"Model", "type": "text"},
                "position":{"label":"Position", "type": "coordinates"},
                "speed": {"label":"Average speed", "type": "number"}},
            "Flight": {
                "id": {"label":"Flight number", "type": "text"},
                "airplane": {"label":"Airplane", "type": "Airplane"},
                "origin":{"label":"Origin", "type": "Airport"},
                "destination":{"label":"Destination", "type": "Airport"},
                "departure":{"label":"Departure time", "type": "datetime"}}}
    ##@var selection
    #Current selected object.
    selection = None
    #TODO: replace "Airport" by Airport.__name__
    
    def __init__(self, gui):
        """GUI initialization"""
        self.app = gui 
        self.app.setTitle(self.__appname)
        self.app.setSize(800, 600)
        #Panel
        self.app.setSticky("nw")
        self.app.startFrame(title="panel", row=0, column=0)
        #Panel - Info
        self.app.startLabelFrame(title="info", row=0, column=0)
        self.app.setSticky("new")
        row = 0
        for elementtype in self.elements:
            self.app.addLabel(elementtype + "s: ", row=row, column=0)
            self.app.addLabel(elementtype, row=row, column=1)
            self.app.addNamedButton("Add " + elementtype, self.add.__name__ + self.__separator + elementtype, self.add, row=row, column=2)
            row += 1
        self.updateInfo()
        self.app.stopLabelFrame()
        #Panel - Legend
        self.app.startLabelFrame(title="Legend", row=1, column=0)
        self.app.setSticky("new")
        self.app.addLabel("Commercial")
        self.app.setLabelBg("Commercial", "Blue")
        self.app.addLabel("Military")
        self.app.setLabelBg("Military", "Red")
        self.app.stopLabelFrame()
        #Panel - Selection
        self.app.startLabelFrame(title="Selection", row=2, column=0)
        self.app.setSticky("new")
        self.app.addLabel("Selection")
        self.app.addButton("Delete", self.delete)
        self.app.stopLabelFrame()
        self.app.stopFrame()
        #Chart
        global chart
        chart = chart.Chart(self.app, 0, 1)
        #self.app launching
        print(self.__appname + " initialized")
        self.app.go()
        
    def add(self, button):
        """It launches the form window to add a new element to the map
            @param button    button name from the panel previously pressed
        """
        elementtype = button[len(self.add.__name__ + self.__separator):]
        self.app.startSubWindow(elementtype, modal=True)
        for field in self.info[elementtype]:
            self.app.addLabel(field + self.__separator + "label", text=self.info[elementtype][field]["label"], column=0)
            fieldtype = self.info[elementtype][field]["type"]
            if fieldtype == "text":
                self.app.addEntry(field, column=1)
            elif fieldtype == "number":
                self.app.addNumericEntry(field, column=1)
            elif fieldtype == "datetime":
                self.app.addDatePicker(field, column=1, date=datetime.now())
            elif fieldtype == "Airport":
                self.app.addLabelOptionBox(field, list(self.elements["Airport"].keys()), column=1)
            elif fieldtype == "Airplane":
                self.app.addLabelOptionBox(field, list(self.elements["Airplane"].keys()), column=1)
        self.app.addNamedButton("Submit " + elementtype, self.submit.__name__ + self.__separator + elementtype, self.submit)
        self.app.stopSubWindow()
        self.app.showSubWindow(elementtype)
        print("Showing window to add " + elementtype.lower())
    
    def submit(self, button):
        """It adds a new element to the chart according to the data filled in the form window
            @param button    button name from the form window previously pressed
        """
        elementtype = button[len(self.submit.__name__ + self.__separator):]
        print("Adding " + elementtype.lower())
        data = self.app.getAllInputs()
        for field in data:
            fieldtype = self.info[elementtype][field]["type"]
            if fieldtype == "Airport" | fieldtype == "Airplane":
                data[field] = self.elements[fieldtype][data[field]]
        self.app.destroySubWindow(elementtype)
        self.elements[elementtype][data["id"]] = globals()[elementtype](data)
    
    def delete(self):
        """It deletes the selected element from the chart"""
        if(self.selection):
            print("Showing deletion confirmation dialog")
            if self.app.yesNoBox("Delete object", "Do you want to delete the " (self.selection.__class__.__name__).lower() + " " + self.selection.id + "?"):
                print("Deleting " + (self.selection.__class__.__name__).lower() + " " + self.selection.id)
                del self.elements[self.selection.__class__.__name__][self.selection.id]
            else:
                print("Canceling deletion")
        
    def select(self, elementtype, elementid):
        """It selects an element from the chart to show information on the panel
            @param elementtype    Class of the element
            @param elementid      ID of the element
        """
        if elementtype == None | elementid == None:
            self.selection = self.elements[elementtype][elementid]
            self.app.openFrame("Selection")
            for field in self.info[elementtype]:
                self.app.addLabel(field + self.__separator + "label", text=self.info[elementtype][field]["label"], column=0)
                self.app.addLabel(field, text=str(getattr(self.selection, field)), column=1)
            self.app.stopFrame
            print(type + " " + self.selection.id + " selected")
        else:
            self.selection = None
            print("No element is selected now")
    
    def updateInfo(self):
        """It updates the info panel."""
        for elementtype in self.elements:
            if self.elements[elementtype]:
                self.app.setLabel(elementtype, len(self.elements[elementtype]))
            else:
                self.app.setLabel(elementtype, 0)
    
    def updateChart(self):
        """It refreshes the chart."""
        self.chart.clear()
        for elementtype in self.elements:
            for element in elementtype:
                self.chart.add(element)
        #TODO: refreshing
        
