from ProjectConstants import *
from Sprite import Sprite
import random
import time


class MenuFun:
	def __init__(self, centerX, centerY, dotSpeed):
		self.originalCenterX = centerX
		self.originalCenterY = centerY
		self.currentCenterX = centerX
		self.currentCenterY = centerY
		self.angle = degrees_to_mouse(self.originalCenterX, self.originalCenterY)  #degrees
		self.dotSpeed = dotSpeed

		self.dotRadius = 25
		self.dot = pygame.image.load('images/purple dot.svg').convert_alpha()
		self.scaled_dot = pygame.transform.scale(self.dot, (2 * self.dotRadius, 2 * self.dotRadius)).convert_alpha()

		self.dots: list[Sprite] = []
		self.arrowLength = 50

	def change_angle(self):
		self.angle = degrees_to_mouse(self.originalCenterX, self.originalCenterY)

	def draw_static(self, screen):

		self.change_angle()

		blit_center(screen, self.scaled_dot, (self.originalCenterX, self.originalCenterY))

		#draw arrow
		arrowLayer = pygame.Surface((200, 200)).convert_alpha()  #center is on center of mass
		arrowLayer.fill((0, 0, 0, 0))

		pygame.draw.rect(arrowLayer, objectsColor, (100 + self.dotRadius + 10, 97, self.arrowLength, 6))
		pygame.draw.polygon(arrowLayer, objectsColor, ((100 + self.dotRadius + 10 + self.arrowLength, 90),
													   (100 + self.dotRadius + 10 + self.arrowLength + 10, 100),
													   (100 + self.dotRadius + 10 + self.arrowLength, 110)))

		rotatedSurface, center = rotate_surface(arrowLayer, self.angle, self.currentCenterX, self.currentCenterY)

		screen.blit(rotatedSurface, center)

		#if mouse is clicked, add a new dot to dot list
		if ifClicked():
			self.dots.append(Sprite(self.scaled_dot, self.currentCenterX, self.currentCenterY, self.dotSpeed, self.angle, "circle", 0.8))

		#draw all dots
		for dot in self.dots:
			dot.draw_static(screen)

		#remove sprites that are past boundaries of screen
		self.dots = [dot for dot in self.dots if 0 < dot.get_centerX() < SCREEN_WIDTH and 0 < dot.get_centerY() < SCREEN_HEIGHT]

		#draw arrow
		arrowLayer = pygame.Surface((200, 200)).convert_alpha()  #center is on center of mass
		arrowLayer.fill((0, 0, 0, 0))

		pygame.draw.rect(arrowLayer, objectsColor, (100 + self.dotRadius + 10, 97, self.arrowLength, 6))
		pygame.draw.polygon(arrowLayer, objectsColor, ((100 + self.dotRadius + 10 + self.arrowLength, 90),
													   (100 + self.dotRadius + 10 + self.arrowLength + 10, 100),
													   (100 + self.dotRadius + 10 + self.arrowLength, 110)))

		rotatedSurface, center = rotate_surface(arrowLayer, self.angle, self.currentCenterX, self.currentCenterY)

		screen.blit(rotatedSurface, center)
