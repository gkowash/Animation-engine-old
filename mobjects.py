from vec2d import *
from game_tools import *
from transformations import *

class Mobject:
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.currentMovements = []
        self.mobjects = []
        self.params.update(kwargs)
        for name, value in self.params.items():
            if type(value) == list or type(value) == tuple:
                value = np.array(value)
            setattr(self, name, value)
    def toPixel(self, coords):
        return self.parent.toPixel(coords)
    def move(self):
        for movement in self.currentMovements:
            movement.step()
            if movement.t >= movement.time:
                self.currentMovements.remove(movement)
    def rotateBy(self, angle, axis, time, delay=0, ratefunc=SmoothMove()):
        self.currentMovements.append(
            Rotation(
                parent = self,
                angle = angle,
                axis = axis,
                time = time,
                delay = delay,
                ratefunc = ratefunc
                )
            )
    def changeColorTo(self, endColor, time, delay=0, ratefunc=ConstantRF()):
        self.currentMovements.append(
            ChangeColor(
                parent = self,
                endColor = endColor,
                time = time,
                delay = delay,
                ratefunc = ratefunc
            )
        )

class Line(Mobject):
    params = {
        'start': (0, 0),
        'end': (10, 10),
        'color': white,
        'width': 0.001,
        'draw_start_arrow': False,
        'draw_end_arrow': False,
        'arrowWidth': 0.1,
        'arrowLength': 0.15
    }

    def __init__(self, parent, **kwargs):
        Mobject.__init__(self, parent, **kwargs)
        self.update_vectors()
        self.end_arrow_base = self.end - self.arrowLength * self.unit_vector  # need to restructure this a bit
        # self.create_arrows()  #need to include 'Triangle' class first
        self.update_vertices()

    def update_vectors(self):
        self.vector = r_vec(self.start, self.end)
        self.unit_vector = norm(r_vec(self.start, self.end))
        self.normal_vector = rotate(self.unit_vector, np.pi / 2)

    def update_vertices(self):
        self.update_vectors()
        self.end_arrow_base = self.end - self.arrowLength * self.unit_vector

        p1 = self.end_arrow_base + self.width / 2 * self.normal_vector
        p2 = self.end_arrow_base - self.width / 2 * self.normal_vector
        p3 = self.start - self.width / 2 * self.normal_vector
        p4 = self.start + self.width / 2 * self.normal_vector

        self.vertices = np.array([p1, p2, p3, p4])
        self.midpoint = self.get_midpoint()
        if self.draw_start_arrow:
            self.start_arrow.vertices = self.get_start_arrow_vertices()
        if self.draw_end_arrow:
            self.end_arrow.vertices = self.get_end_arrow_vertices()

    def get_midpoint(self):
        return self.start + (self.end - self.start) / 2

    def get_start_arrow_vertices(self):
        return np.array([self.start_arrow_base + self.normal_vector * self.arrowWidth,
                         self.start_arrow_base - self.normal_vector * self.arrowWidth,
                         self.start_arrow_base + self.unit_vector * self.arrowLength])

    def get_end_arrow_vertices(self):
        return np.array([self.end_arrow_base + self.normal_vector * self.arrowWidth,
                         self.end_arrow_base - self.normal_vector * self.arrowWidth,
                         self.end_arrow_base + self.unit_vector * self.arrowLength])

    def create_arrows(self):
        if self.draw_start_arrow:
            self.start = self.start + self.unit_vector * self.arrowLength
            self.start_arrow = Triangle(params={'vertices': self.get_start_arrow_vertices(), 'color': self.color})
        if self.draw_end_arrow:
            self.end_arrow = Triangle(params={'vertices': self.get_end_arrow_vertices(), 'color': self.color})

    def move(self):
        self.pointlist = np.array([self.start, self.end])
        Mobject.move(self)
        self.start, self.end = self.pointlist

        self.update_vertices()

    def draw(self, display):
        color = self.color.astype(int)

        if self.draw_start_arrow:
            self.start_arrow.color = color
        if self.draw_end_arrow:
            self.end_arrow.color = color

        # converted_vertices = list(map(lambda x: parent.toPixel().astype(int), self.vertices))

        convertedPoints = []
        for vertex in self.vertices:
            convertedPoints.append(
                self.parent.toPixel(vertex).astype(int))  # make it so 'toPixel' can handle arrays of coordinates

        pygame.gfxdraw.aapolygon(display, convertedPoints, color)
        pygame.gfxdraw.filled_polygon(display, convertedPoints, color)

        # if self.draw_start_arrow:

        #     self.start_arrow.draw(graph)
        # if self.draw_end_arrow:
        #     self.end_arrow.draw(graph)


class Circle(Mobject):
    params = {
        'center': (0, 0),
        'radius': 1,
        'color': white,
        'width': 1,  # use width=0 to fill shape
        'resolution': 100  # number of points
    }

    def __init__(self, parent, **kwargs):
        Mobject.__init__(self, parent, **kwargs)
        self.update_points()
        if self.width == 0:
            self.filled = True
        else:
            self.filled = False

    def update_points(self):
        angles = np.linspace(0, 2 * np.pi, self.resolution)
        self.points = self.radius * np.transpose(np.array([np.cos(angles), np.sin(angles)]))

    def draw(self, display):  # needs work
        points = []
        for point in self.points:
            points.append(self.parent.toPixel(point).astype(int))
        if self.filled:
            gfxdraw.filled_polygon(display, points, self.color)
        else:
            gfxdraw.aapolygon(display, points, self.color)