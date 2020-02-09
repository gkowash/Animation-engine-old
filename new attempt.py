import pygame
import numpy as np
from pygame import gfxdraw
from vec2d import *
from game_tools import *
from ratefunctions import *
from transformations import *
from graphing import *
from blocking import *
from elements import *

#initialize clock
fps = 30
clock = pygame.time.Clock()

#initialize window
myWindow = Window(
    displaySize = (700,700)  #size in pixels
)

#initialize camera
myCam = Camera(
    window=myWindow,
    pos=(0.50, 0.50),
    zoom=0.80
)

#initialize main canvas
myCanvas = Element(
    parent = myWindow,
    pos = (0,0),
    dim = (1,1)
)



#create scene (contains directions for constructing and animating scene)
class TestScene:
    def __init__(self):
        #temporary timer variable to control camera movement
        self.t = 0
        #initialize subcanvases/scene elements
        self.graph = myCanvas.add_graph(
            pos = (0.01, 0.01),   #as fraction of full width/height
            dim = (0.98, 0.98),
            xRange = (-5, 5),
            yRange = (-5, 5),
            tickInterval = 2,
            gridlineColor = (40, 40, 70),
            axisColor = (180, 180, 180),
            tickColor = (180, 180, 180)
        )

        self.line = self.graph.add_line(
            start = (-5, 5),
            end = (-2, 0),
            color = (68, 218, 235)
        )

        #
        # center = (-3,0)
        # focus = (3,0)
        # radius = 4
        #
        # self.lines = []
        # for theta in np.arange(0, 2*np.pi, np.pi/50):
        #     endpoint = vec(radius, theta)
        #     line = self.graph.add_line(
        #         start = focus,
        #         end = endpoint,
        #         color = red
        #     )
        #     self.lines.append(line)


    def seg1(self):
        self.line.rotateBy(
            angle = -np.arctan(3/5),
            axis = self.line.start,
            time = 45
            )
        myCam.zoomTo(1.4, 100, delay=15)
        myCam.panTo((-1.7,0), 60, coordFrame=self.graph)
        self.show(60)
        # d = 30
        # for line in self.lines:
        #     line.rotateBy(np.pi/2, line.midpoint, 60, delay=d)
        #     line.changeColorTo(violet, 60, delay=d)
        #     d += 1

    def seg2(self):
        self.line.rotateBy(
            angle = -np.pi/2,
            axis = self.line.end,
            time = 45
        )
        self.line.changeColorTo(
            (179, 236, 242),
            45
        )

        self.show(60)
        # d = 15
        # for line in reversed(self.lines):
        #     line.rotateBy(np.pi/2, line.midpoint, 60, delay=d+40)
        #     line.changeColorTo(red, 60, delay=d)
        #     d += 1

    def seg3(self):
        self.line.rotateBy(
            angle = 4 * np.pi,
            axis = self.line.midpoint,
            time = 150
        )
        self.line.rotateBy(
            angle = np.pi/2,
            axis = (0,2),
            time = 150
        )
        myCam.zoomTo(9, 150)
        myCam.panTo((-1.7,-0.3), 120, coordFrame=self.graph)
        self.show(180)
        print("Segment 3 end")

    def show(self, frames):
        for i in range(frames):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
            myWindow.display.fill(black)
            for element in myCanvas.elements:
                element.update()
                element.draw(myWindow.display)
            myCam.update()
            pygame.display.flip()
            clock.tick(fps)
            self.t += 1
    def play(self):
        self.seg1()
        print('Segment 1 end')
        self.seg2()
        print('Segment 2 end')
        self.seg3()




class TestScene2:
    def __init__(self):
    #temporary timer variable to control camera movement
        self.t = 0
        #initialize subcanvases/scene elements
        self.graph = myCanvas.add_graph(
            pos = (0.01, 0.01),   #as fraction of full width/height
            dim = (0.98, 0.98),
            xRange = (-5, 5),
            yRange = (-5, 5),
            tickInterval = 2,
            gridlineColor = (40, 40, 70),
            axisColor = (180, 180, 180),
            tickColor = (180, 180, 180)
        )

        self.circle = self.graph.add_circle(
            center = (0,0),
            radius = 3,
            color = (68, 218, 235),
            resolution = 300
        )

        #
        # center = (-3,0)
        # focus = (3,0)
        # radius = 4
        #
        # self.lines = []
        # for theta in np.arange(0, 2*np.pi, np.pi/50):
        #     endpoint = vec(radius, theta)
        #     line = self.graph.add_line(
        #         start = focus,
        #         end = endpoint,
        #         color = red
        #     )
        #     self.lines.append(line)


    def seg1(self):
        self.line.rotateBy(
            angle = -np.arctan(3/5),
            axis = self.line.start,
            time = 45
            )
        # d = 30
        # for line in self.lines:
        #     line.rotateBy(np.pi/2, line.midpoint, 60, delay=d)
        #     line.changeColorTo(violet, 60, delay=d)
        #     d += 1

    def seg2(self):
        self.line.rotateBy(
            angle = -np.pi/2,
            axis = self.line.end,
            time = 45
        )
        self.line.changeColorTo(
            (179, 236, 242),
            45
        )
        # d = 15
        # for line in reversed(self.lines):
        #     line.rotateBy(np.pi/2, line.midpoint, 60, delay=d+40)
        #     line.changeColorTo(red, 60, delay=d)
        #     d += 1

    def seg3(self):
        self.line.rotateBy(
            angle = 4 * np.pi,
            axis = self.line.midpoint,
            time = 120
        )
        self.line.rotateBy(
            angle = np.pi/2,
            axis = (0,2),
            time = 120
        )

    def show(self, frames):
        for i in range(frames):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
            myWindow.screen.fill(black)
            for element in myCanvas.elements:
                for mobject in element.mobjects:
                    mobject.move()
                    mobject.draw()
                element.draw()
            pygame.display.flip()
            clock.tick(fps)
            self.t += 1

    def play(self):
       self.show(600)




#testScene2 = TestScene2()
#circle = testScene2.play()

testScene = TestScene()
#myCam.pos = testScene.graph.toParentCoords((0,0))
testScene.play()


        # #initialize mobjects
        # t_v1 = topGraph.add_vector(
        #     pos=(0,0),
        #     angle=pi/4,
        #     mag=5
        # )
        # t_v2 = topGraph.add_vector(
        #     pos=(0,0),
        #     angle=2*pi/3,
        #     mag=3
        # )
        # b_c = botGraph.add_circle(
        #     pos=(6,7),
        #     rad=4
        # )
        # b_rec = botGraph.add_rect(
        #     pos=(-1,3),
        #     dim=(7,2)
        # )
