"""
@package src
@author andresgonzalezfornell

User interface.
"""

from src import chart
from dataclasses import field

from src.core import *  #TODO: change core @UnusedWildImport


class App:
    """Class of the user interface."""

    ##@var __appname
    #Name of the self.application
    __appname = "Air traffic control"
    ##@var __refresh
    #Period time in seconds to refresh the chart
    __refresh = 1
    ##@var separator
    #Character to separate some strings for widget names
    separator = "_"
    ##@var app
    #appJar GUI object
    app = None
    ##@var chart
    #Chart object
    chart = chart.Chart(app)
    ##@var elements
    #Sets of existing elements.
    elements = {Airport.__name__ : {}, Airplane.__name__ : {}, Flight.__name__ : {}}
    ##@defgroup GUI widgets names
    ##@{
    panel = "panel"
    panel_legend = "Legend"
    panel_elements = "Elements"
    panel_elements_add = "add"
    panel_elements_add_error = "errorbox"
    panel_actions = "Actions"
    panel_actions_delete = "delete"
    panel_actions_start = "start"
    panel_elements_select = "select"
    panel_elements_select_selector = "selector"
    panel_elements_select_selector_elementtype = "elementtype"
    panel_elements_select_selector_ident = "ident"
    panel_info = "Selection"
    ##}
    
    class Field:
        """Field from an object of type Airport, Airplane or Flight"""
        ##@var name
        #Unique name which identifies the form field and the class attribute or method. 
        name = None
        ##@var description
        #Field description which will show on the user interface.
        description = None
        ##@var fieldtype
        #Field type (text, number or class name). It corresponds to a list if the field is a list of values.
        fieldtype = "text"
        ##@var factor
        #If field type is number, factor multiplies the field value
        factor = None
        
        def __init__(self, name, description, fieldtype, factor=None):
            self.name = name
            self.description = description
            self.fieldtype = fieldtype
            if self.fieldtype == "number":
                self.factor = factor
    
    class Input(Field):
        """Input field from an object of type Airport, Airplane or Flight"""
        pass
    
    class Output(Field):
        """Output field from an object of type Airport, Airplane or Flight"""
        pass
        
    ##@var inputs
    #Relevant fields to create a new object 
    inputs = {Airport.__name__: {
                "ident":Input("ident", "Airport code", "text"),
                "location":Input("location", "Location", [
                    Input("longitude", "Longitude [°]", "number"),
                    Input("latitude", "Latitude [°]", "number")]),
                "industry":Input("industry", "Industry", "Industry")},
              Airplane.__name__: {
                "ident":Input("ident", "Plate", "text"),
                "location":Input("location", "Location", Airport.__name__),
                "industry":Input("industry", "Industry", "Industry"),
                "manufacturer":Input("manufacturer", "Manufacturer", "text"),
                "model":Input("model", "Model", "text"),
                "speed":Input("speed", "Average speed [km/h]", "number", factor=1 / 3.6)},
              Flight.__name__: {
                "ident":Input("ident", "Flight number", "text"),
                "airplane":Input("airplane", Airplane.__name__, Airplane.__name__),
                "origin":Input("origin", "Origin", Airport.__name__),
                "destination":Input("destination", "Destination", Airport.__name__)}}
    ##@var outputs
    #Relevant outputs of the selected object to show on the selection panel
    outputs = {Airport.__name__: {
                "ident":Output("ident", "Plate", "text"),
                "location":Output("location", "Location", [
                    Output("longitude", "Longitude [°]", "number"),
                    Output("latitude", "Latitude [°]", "number")]),
                "industry":Output("industry", "Industry", "Industry")},
               Airplane.__name__: {
                "ident":Output("ident", "Plate", "text"),
                "location":Output("location", "Location", [
                    Output("longitude", "Longitude [°]", "number"),
                    Output("latitude", "Latitude [°]", "number")]),
                "industry":Output("industry", "Industry", "Industry"),
                "manufacturer":Output("manufacturer", "Manufacturer", "text"),
                "model":Output("model", "Model", "text"),
                "speed":Output("speed", "Average speed [km/h]", "number", factor=3.6)},
               Flight.__name__: {
                "ident":Output("ident", "Flight number", "text"),
                "airplane":Output("airplane", Airplane.__name__, Airplane.__name__),
                "origin":Output("origin", "Origin", Airport.__name__),
                "destination":Output("destination", "Destination", Airport.__name__),
                "calculateDistance":Output("distance", "Total distance [km]", "number", factor=1E3),
                "calculateTime":Output("time", "Total time [h]", "number", factor=60 * 60),
                "calculateETA":Output("eta", "Time to arrival [h]", "number", factor=60 * 60)}}
    ##@var selection
    #Current selected object.
    selection = None
    
    def __init__(self, gui):
        """GUI initialization."""
        self.app = gui 
        self.app.setTitle(self.__appname)
        self.app.setSize(800, 600)
        #Panel
        self.app.setSticky("nw")
        self.app.startFrame(title="panel", row=0, column=0)
        #Panel - Legend
        self.app.startLabelFrame(title=self.panel_legend, row=0, column=0)
        self.app.setSticky("new")
        self.app.addLabel("Commercial")  #TODO: gets from Industry class
        self.app.setLabelBg("Commercial", "Blue")
        self.app.addLabel("Military")
        self.app.setLabelBg("Military", "Red")
        self.app.stopLabelFrame()
        #Panel - Elements
        self.app.startLabelFrame(title=self.panel_elements, row=1, column=0)
        self.app.setSticky("new")
        row = 0
        for elementtype in self.elements:
            self.app.addLabel(elementtype + "s: ", row=row, column=0)
            self.app.addLabel(elementtype, row=row, column=1)
            self.app.addNamedButton("Add " + elementtype, self.panel_elements_add + self.separator + elementtype, self.add, row=row, column=2)
            row += 1
        self.app.addNamedButton("Select", self.panel_elements_select, self.loadSelector, column=2)
        self.app.stopLabelFrame()
        #Panel - Actions
        self.app.startLabelFrame(title=self.panel_actions, row=2, column=0)
        self.app.setSticky("new")
        self.app.stopLabelFrame()
        #Panel - Info
        self.app.startLabelFrame(title=self.panel_info, row=3, column=0)
        self.app.setSticky("new")
        self.app.stopLabelFrame()
        self.app.stopFrame()
        #Chart
        self.chart = chart.Chart(self.app, 0, 1)
        #self.app.registerEvent(self.updateChart) #TODO: enable
        #self.app.setPollTime(self.__refresh)
        #App launching
        self.select(None, None)
        self.updateElements()
        self.updateChart()
        print(self.__appname + " initialized")
        self.app.go()
        
    def add(self, button):
        """It launches the form window to add a new element to the map.
            @param button    button name from the panel previously pressed
        """
        elementtype = button[len(self.add.__name__ + self.separator):]

        def setFields(fields, parent=self.panel_elements_add + self.separator + elementtype):
            """It deploys all the inputs field on the GUI form.
                @param fields    set of properties to extract from the object
                @param parent    parent name to add as prefix to all widgets of the GUI
            """ 
            if isinstance(fields, dict):
                loop = fields
            elif isinstance(fields, list):
                loop = range(0, len(fields))
            else:
                raise ValueError("Argument fields must be a dictionary or list")
            row = 0
            for index in loop:
                field = fields[index]
                if isinstance(field, self.Input):
                    name = parent + self.separator + field.name
                    self.app.addLabel(name + self.separator + "description", text=field.description, column=0)
                    if isinstance(field.fieldtype, dict) | isinstance(field.fieldtype, list):
                        self.app.startFrame(name, row=row, column=1)
                        setFields(field.fieldtype, parent=name)
                        self.app.stopFrame()
                    else:
                        if field.fieldtype == "text":
                            self.app.addEntry(name, row=row, column=1)
                        elif field.fieldtype == "number":
                            self.app.addNumericEntry(name, row=row, column=1)
                        elif field.fieldtype == "Industry":
                            self.app.addOptionBox(name, ["commercial", "military"], row=row, column=1)  #TODO: change to Industry method
                        elif field.fieldtype == Airport.__name__:
                            self.app.addOptionBox(name, self.elements[Airport.__name__], row=row, column=1)
                        elif field.fieldtype == Airplane.__name__:
                            self.app.addOptionBox(name, self.elements[Airplane.__name__], row=row, column=1)
                row += 1
        
        try:
            self.app.startSubWindow(self.panel_elements_add + self.separator + elementtype, modal=True)
        except:
            self.app.destroySubWindow(self.panel_elements_add + self.separator + elementtype)
            self.app.startSubWindow(self.panel_elements_add + self.separator + elementtype, modal=True)
        self.app.emptyCurrentContainer()
        setFields(self.inputs[elementtype])
        self.app.addNamedButton("Submit", self.panel_elements_add + self.separator + elementtype + self.separator + self.submit.__name__, self.submit, column=1)
        self.app.stopSubWindow()
        self.app.showSubWindow(self.panel_elements_add + self.separator + elementtype)
        print("Showing window to add " + elementtype.lower())
    
    def submit(self, button):
        """It adds a new element to the chart according to the data filled in the form window.
            @param button    button name from the form window previously pressed
        """
        elementtype = button[len(self.panel_elements_add + self.separator):-len(self.separator + self.submit.__name__)]

        def getProperties(fields, parent=self.panel_elements_add + self.separator + elementtype):
            """It collects all input values from the GUI form and returns them as a dictionary set.
                @param fields    set of properties to extract from the object
                @param parent    parent name to add as prefix to all widgets of the GUI
            """
            if isinstance(fields, dict):
                properties = {}
                loop = fields
            elif isinstance(fields, list):
                properties = [None] * len(fields)
                loop = range(0, len(fields))
            else:
                raise ValueError("Argument fields must be a dictionary or list")
            for index in loop:
                field = fields[index]
                if isinstance(field, self.Input):
                    if isinstance(field.fieldtype, dict) | isinstance(field.fieldtype, list):
                        properties[index] = getProperties(field.fieldtype, parent + self.separator + field.name)
                        if properties[index] == None:
                            return None
                    else:
                        if (parent + self.separator + field.name) in self.app.getAllInputs():
                            value = self.app.getAllInputs()[parent + self.separator + field.name]
                            if field.fieldtype == "text":
                                properties[index] = str(value)
                            elif field.fieldtype == "number":
                                factor = 1
                                if not field.factor is None:
                                    factor = field.factor
                                properties[index] = factor * float(value)
                            elif field.fieldtype == "Industry":
                                properties[index] = str(value)
                            elif field.fieldtype == Airport.__name__:
                                properties[index] = self.elements[Airport.__name__][str(value)]
                            elif field.fieldtype == Airplane.__name__:
                                properties[index] = self.elements[Airplane.__name__][str(value)]
                        else:
                            return None
            return properties

        print("Adding " + elementtype.lower())
        properties = getProperties(self.inputs[elementtype])
        self.app.destroySubWindow(self.panel_elements_add + self.separator + elementtype)
        if properties != None:
            if elementtype == Airport.__name__:
                self.elements[elementtype][properties["ident"]] = Airport(properties)
            elif elementtype == Airplane.__name__:
                self.elements[elementtype][properties["ident"]] = Airplane(properties)
            elif elementtype == Flight.__name__:
                self.elements[elementtype][properties["ident"]] = Flight(properties)
            self.chart.add(self.elements[elementtype][properties["ident"]])
            self.updateElements()
            self.select(elementtype, properties["ident"])
        else:
            print("Error: some imputs are empty")
            self.app.errorBox(self.panel_elements_add_error, "All input data must be filled to add " + str.lower(elementtype) + ".")
        
    def select(self, elementtype, ident):
        """It selects an element to show information on the selection panel.
            @param elementtype    element type
            @param ident          element id
        """

        def setProperties(fields, parent="selection", listattribute=None):
            """It gets the attributes from the object and deploys the information on the GUI.
                @param fields           set of properties to extract from the object
                @param parent           parent name to add as prefix to all widgets of the GUI
                @param listattribute    attribute to get list value if the fields are a list
            """
            if isinstance(fields, dict):
                listattribute = None
                loop = fields
            elif isinstance(fields, list):
                if listattribute == None:
                    raise ValueError("When the fields argument is a list, the argument list must be passed")
                loop = range(0, len(fields))
            else:
                raise ValueError("Argument fields must be a dictionary or list")
            row = 0
            for index in loop:
                field = fields[index]
                if isinstance(field, self.Output):
                    name = parent + self.separator + field.name
                    self.app.addLabel(name + self.separator + "description", text=field.description, row=row, column=0)
                    if isinstance(field.fieldtype, dict):
                        self.app.startFrame(name, row=row, column=1)
                        setProperties(field.fieldtype, parent=name)
                        self.app.stopFrame()
                    elif isinstance(field.fieldtype, list):
                        self.app.startFrame(name, row=row, column=1)
                        setProperties(field.fieldtype, parent=name, listattribute=index)
                        self.app.stopFrame()
                    else:
                        # Lists
                        if listattribute == None:
                            value = getattr(self.selection, index)
                        else:
                            value = getattr(self.selection, listattribute)[index]
                        # Functions
                        if callable(value):
                            value = value()
                        # Value types
                        if field.fieldtype == "number":
                            if field.factor != None:
                                value = field.factor * value                            
                        elif (field.fieldtype == Airport.__name__) | (field.fieldtype == Airplane.__name__):
                            value = value.ident
                        # Value
                        self.app.addLabel(name, text=str(value), row=row, column=1)
                    row += 1

        self.app.openLabelFrame(self.panel_actions)
        self.app.emptyCurrentContainer()
        self.app.stopLabelFrame()
        if (elementtype != None) & (ident != None):
            self.selection = self.elements[elementtype][ident]
            self.app.openLabelFrame(self.panel_info)
            self.app.emptyCurrentContainer()
            setProperties(self.outputs[elementtype])
            self.app.stopLabelFrame()
            self.app.openLabelFrame(self.panel_actions)
            self.app.addNamedButton("Delete", self.panel_actions_delete, self.delete)
            if (elementtype == Flight.__name__):
                self.app.addNamedButton("Start", self.panel_actions_start, self.start)
            print(elementtype + " " + self.selection.ident + " selected")
            self.app.stopLabelFrame()
        else:
            self.selection = None
            self.app.openLabelFrame(self.panel_info)
            self.app.emptyCurrentContainer()
            self.app.stopLabelFrame()
            print("No element is selected now")
        
    def start(self):
        """It starts a flight."""
        if self.selection != None:
            if self.selection.__class__.__name__ == Flight.__name__:
                print("Starting selected flight")
                self.selection.start()

    def delete(self):
        """It deletes the selected element from the chart."""
        if self.selection != None:
            print("Showing deletion confirmation dialog")
            if self.app.yesNoBox("Delete object", "Do you want to delete the " + str.lower(self.selection.__class__.__name__) + " " + self.selection.ident + "?"):
                print("Deleting " + (self.selection.__class__.__name__).lower() + " " + self.selection.ident)
                del self.elements[self.selection.__class__.__name__][self.selection.ident]
                self.updateChart()
                self.updateElements()
                self.select(None, None)
            else:
                print("Canceling deletion")
                
    def loadSelector(self):
        """It loads the selector window."""

        def updateSelector():
            """It updates the elements list to select according to the element type choice."""
            elementtype = self.app.getRadioButton("elementtype")
            print("Element type " + elementtype + " chosen")
            self.app.updateListBox(self.panel_elements_select_selector_ident, list(self.elements[elementtype].keys()))
        
        try:
            self.app.startSubWindow(self.panel_elements_select_selector, modal=True)
        except:
            self.app.destroySubWindow(self.panel_elements_select_selector)
            self.app.startSubWindow(self.panel_elements_select_selector, modal=True)
        self.app.emptyCurrentContainer()
        for elementtype in self.elements:
            self.app.addRadioButton(self.panel_elements_select_selector_elementtype, elementtype)
        self.app.setRadioButtonChangeFunction(self.panel_elements_select_selector_elementtype, updateSelector)
        self.app.addListBox(self.panel_elements_select_selector_ident, [])
        self.app.addNamedButton("Submit", self.panel_elements_select_selector + self.separator + self.submitSelector.__name__, self.submitSelector)
        updateSelector()
        self.app.stopSubWindow()
        self.app.showSubWindow(self.panel_elements_select_selector)
        
    def submitSelector(self):
        """It handles the selection. It is called when pressing the submit button on the selector window."""
        elementtype = self.app.getRadioButton("elementtype")
        if len(self.app.getListBox(self.panel_elements_select_selector_ident)) > 0:
            ident = self.app.getListBox(self.panel_elements_select_selector_ident)[0]
        else:
            ident = None
        self.select(elementtype, ident)
        self.app.destroySubWindow(self.panel_elements_select_selector)
    
    def updateChart(self):
        """It refreshes the chart."""
        for flight in self.elements[Flight.__name__]:
            self.elements[Flight.__name__][flight].elapse(self.__refresh)
        self.chart.clear()
        for elementtype in self.elements:
            for element in self.elements[elementtype]:
                self.chart.add(self.elements[elementtype][element])
                
    def updateElements(self):
        """It updates the elements panel."""
        for elementtype in self.elements:
            if self.elements[elementtype]:
                self.app.setLabel(elementtype, len(self.elements[elementtype]))
            else:
                self.app.setLabel(elementtype, 0)
