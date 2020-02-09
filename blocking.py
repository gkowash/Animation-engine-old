import pygame
import numpy as np
from ratefunctions import *
from transformations import Zoom, Pan

class Window:
    def __init__(self, displaySize):
        self.displaySize = displaySize
        self.display = pygame.display.set_mode(displaySize)
    def toPixel(self, coords):
        #takes in (width, height) as fraction of total size and returns pixel coordinates
        return self.camera.toPixel(coords)

class Camera:
    def __init__(self, window, pos, zoom):
        self.pos = np.array(pos)
        self.zoom = zoom
        self.window = window
        self.movements = []
        window.camera = self
    def update(self):
        for movement in self.movements:
            movement.step()
            if movement.t >= movement.duration:
                self.movements.remove(movement)
    def toPixel(self, coords):
        topLeft = self.pos - (1/self.zoom) / 2 #top left corner of camera viewport in window frame
        newCoords = (coords - topLeft) * self.zoom #coordinate's position relative to top left in camera frame
        return self.window.displaySize * newCoords #convert to pixels
    def zoomBy(self, amount, duration, delay=0, ratefunc=SmoothMove()):
        self.movements.append(Zoom(
            camera = self,
            amount = amount,
            duration = duration,
            delay = delay,
            ratefunc = ratefunc
        ))

    def zoomTo(self, endValue, duration, delay=0, ratefunc=SmoothMove()):
        amount = endValue - self.zoom
        self.movements.append(Zoom(
            camera = self,
            amount = amount,
            duration = duration,
            delay = delay,
            ratefunc = ratefunc
        ))

    #currently does not pan by correct amount
    def panBy(self, change, duration, delay=0, ratefunc=SmoothMove(), coordFrame=None):
        if coordFrame == None:
            change = np.array(change)
        else:
            change = coordFrame.toParentCoords(change)
        self.movements.append(Pan(
            camera = self,
            change = np.array(change),
            duration = duration,
            delay = delay,
            ratefunc = ratefunc
        ))
    def panTo(self, endpoint, duration, delay=0, ratefunc=SmoothMove(), coordFrame=None):
        if coordFrame == None:
            change = np.array(endpoint) - self.pos
        else:
            endpoint = coordFrame.toParentCoords(endpoint)
            change = endpoint - self.pos
        self.movements.append(Pan(
            camera = self,
            change = change,
            duration = duration,
            delay = delay,
            ratefunc = ratefunc
        ))