import pygame
from ProjectConstants import *


class SliderBar:
	def __init__(self, x, y, width, height, minValue, maxValue, defaultValue):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.minValue = minValue
		self.maxValue = maxValue
		self.valueRange = maxValue - minValue
		self.value = defaultValue
		self.handleWidth = height // 2
		self.handlePos = self.value_to_pos(defaultValue)
		self.handleSelected = False

	def value_to_pos(self, value):
		pos_range = self.width - self.handleWidth
		return int(pos_range * (value - self.minValue) / self.valueRange)

	def pos_to_value(self, pos):
		pos_range = self.width - self.handleWidth
		return int(pos * self.valueRange / pos_range + self.minValue)

	def draw(self, surface):
		mousePos = pygame.mouse.get_pos()

		#if mouse is on handle and is pressed
		if pygame.mouse.get_pressed()[0] == 1:
			if self.x <= mousePos[0] <= self.x + self.width and self.y <= mousePos[1] <= self.y + self.height:
				self.handleSelected = True
				self.handlePos = min(max(mousePos[0] - self.x - self.handleWidth // 2, 0), self.width - self.handleWidth)
				self.value = self.pos_to_value(self.handlePos)
			elif self.handleSelected:
				self.handlePos = min(max(mousePos[0] - self.x - self.handleWidth // 2, 0), self.width - self.handleWidth)
				self.value = self.pos_to_value(self.handlePos)
		else:
			self.handleSelected = False

		# Draw the bar
		bar_rect = pygame.Rect(self.x, self.y + self.height // 2 - 1, self.width, 2)
		pygame.draw.rect(surface, sliderBarColor, bar_rect)

		# Draw the handle
		handle_rect = pygame.Rect(self.x + self.handlePos, self.y, self.handleWidth, self.height)
		pygame.draw.rect(surface, sliderBarHandleColor, handle_rect)

		font = pygame.font.SysFont("jost700", 40)
		text = font.render(str(self.value), True, textColor)
		surface.blit(text, (self.x, self.y))
