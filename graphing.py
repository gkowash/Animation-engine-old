from vec2d import *
from game_tools import *
from mobjects import *


class Axis(Mobject):
    params = {
        'angle': 0,
        'tickInterval': 1,
        'gridlineInterval': 1,
        'domain': (-10,10),
        'name': None
        }

    def __init__(self, parent, **kwargs):
        Mobject.__init__(self, parent, **kwargs)
        self.create_axis()
        self.create_ticks()
        self.create_gridlines()
    def create_axis(self):
        self.axisLine = Line(
            parent = self,
            start = vec(self.domain[0], self.angle),
            end = vec(self.domain[1], self.angle),
            width = 0.01,
            color = self.axisColor,
            arrowLength = 0
            )
    def create_ticks(self):
        self.ticks = []
        for n in np.arange(self.domain[0], self.domain[1]+self.tickInterval, self.tickInterval):
            if n != 0:
                self.ticks.append(Tick(
                    parent = self,
                    pos = vec(n, self.angle),
                    angle = self.angle + np.pi/2,
                    color = self.tickColor
                    ))
    def create_gridlines(self):
        self.gridlines = []
        for n in np.arange(self.domain[0], self.domain[1]+self.gridlineInterval, self.gridlineInterval):
            if n!= 0:
                self.gridlines.append(Gridline(
                    parent = self,
                    pos = vec(n, self.angle),
                    angle = (self.angle + np.pi/2) % np.pi, #prevents angle being set to pi
                    color = self.gridlineColor,
                    domain = self.domain,
                    extent = self.extent
                    ))
    def draw(self, display):
        for gridline in self.gridlines:
            gridline.draw(display)
        self.axisLine.draw(display)
        for tick in self.ticks:
            tick.draw(display)
class Tick(Mobject):
    params = {
        'pos': (0,0),
        'length': 0.2,
        'angle': 0
        }

    def __init__(self, parent, **kwargs):
        Mobject.__init__(self, parent, **kwargs)
        self.create_line()

    def create_line(self):
        start = self.pos + vec(self.length/2, self.angle)
        end = self.pos - vec(self.length/2, self.angle)
        self.line = Line(self,
                         start = start,
                         end = end,
                         color = self.color
                         )

    def draw(self, display):
        self.line.draw(display)

class Gridline(Mobject):
    params = {
        'pos': (0,0),
        'domain': (-10, 10),
        'extent': (-10, 10), #how far gridlines reach perpendicular to axis (mentioned above)
        'angle': 0,
        }

    def __init__(self, parent, **kwargs):
        Mobject.__init__(self, parent, **kwargs)
        self.create_line()

    def create_line(self):
        start = self.pos + vec(self.extent[0], self.angle)
        end = self.pos + vec(self.extent[1], self.angle)
        self.line = Line(
            parent = self,
            start = start,
            end = end,
            color = self.color
            )

    def draw(self, display):
        self.line.draw(display)