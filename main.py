""" 
@package main
@author andresgonzalezfornell

Main module to run the application.
"""

from lib.appJar.appjar import gui
from src.app import App

gui = gui()
gui.setImageLocation("res")
gui.setIcon("airplane.gif")
app = App(gui)