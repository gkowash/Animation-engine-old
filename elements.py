import numpy as np
from vec2d import *
from game_tools import *
from graphing import *

class Element:
    params = {}
    def __init__(self, parent, pos, dim, **kwargs):
        #pos: top-left, dim: width-height, expressed as fraction of parent elements
        self.parent = parent
        self.pos = pos
        self.dim = dim
        self.elements = [] #contains subelements
        self.mobjects = []
        self.params.update(**kwargs)
        for name, value in self.params.items():
            if type(value) == list or type(value) == tuple:
                value = np.array(value)
            setattr(self, name, value)
    def toParentCoords(self, coords):
        return self.pos + coords * self.dim
    def toPixel(self, coords):
        return self.parent.toPixel(self.toParentCoords(coords))
    def update(self):
        for mobject in self.mobjects:
            mobject.move()
    def add_graph(self, pos, dim, **kwargs):
        graph = Graph(self, pos, dim, **kwargs)
        self.elements.append(graph)
        return graph




class Graph(Element):
    params = {
        'xRange': (-10,10),
        'yRange': (-10, 10),
        'xGridlines': 1,
        'yGridlines': 1,
        'curves': [],
        'vectors': [],
        'axisColor': white,
        'gridlineColor': (50,50,50),
        'tickColor': white,
        'tickInterval': 0.5,
        'gridlineInterval': 1
        }
    def __init__(self, parent, pos, dim, **kwargs):
        Element.__init__(self, parent, pos, dim, **kwargs)
        self.create_axes()
    def toParentCoords(self, coords):
        #convert graph coordinates to fraction of total graph dimension, then convert to fraction of parent element
        xMin, xMax = self.xRange
        yMin, yMax = self.yRange
        x, y = coords
        newX = (x - xMin) / (xMax - xMin) * self.dim[0] + self.pos[0]
        newY = (yMax - y) / (yMax - yMin) * self.dim[1] + self.pos[1]  #the 'yMax - y' term is different to flip the y-axis
        return np.array([newX, newY])
    def create_axes(self):
        self.xAxis = Axis(
            parent = self,
            angle = 0,
            domain = self.xRange,
            extent = self.yRange, #how far the gridlines extend perpendicular to the axis (come up with a better name/system for this)
            tickInterval = self.tickInterval,
            gridlineInterval = self.gridlineInterval,
            axisColor = self.axisColor,
            tickColor = self.tickColor,
            gridlineColor = self.gridlineColor,
            name = 'x axis'
            )
        self.yAxis = Axis(
            parent = self,
            angle = np.pi/2,
            domain = self.yRange,
            extent = self.xRange,
            tickInterval = self.tickInterval,
            gridlineInterval = self.gridlineInterval,
            axisColor = self.axisColor,
            tickColor = self.tickColor,
            gridlineColor = self.gridlineColor,
            name = 'y axis'
            )
    def plot_curve(self, params={}):
        self.curves.append(Plot(self, params))
    def plot_vector(self, params):
        self.vectors.append(Vector(params))
    def add_line(self, **kwargs):
        line = Line(parent=self, **kwargs)
        self.mobjects.append(line)
        return line
    def add_circle(self, **kwargs):
        circle = Circle(parent=self, **kwargs)
        self.mobjects.append(circle)
        return circle
    def draw_axes(self, display):
        self.xAxis.draw(display)
        self.yAxis.draw(display)
    def draw_curves(self, display):
        for curve in self.curves:
            curve.draw(self, display)
        for vector in self.vectors:
            vector.draw(self, display)
    def draw(self, display):
        self.draw_axes(display)
        for mobject in self.mobjects:
            mobject.draw(display)