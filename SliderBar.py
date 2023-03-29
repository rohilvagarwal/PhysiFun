import pygame
from ProjectConstants import *


class SliderBar:
	def __init__(self, x, y, width, height, minValue, maxValue, defaultValue):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.min_value = minValue
		self.max_value = maxValue
		self.value_range = maxValue - minValue
		self.value = defaultValue
		self.handle_width = height // 2
		self.handle_pos = self._value_to_pos(defaultValue)
		self.handle_color = sliderBarHandleColor
		self.bar_color = sliderBarColor
		self.handle_rect = pygame.Rect(self.x + self.handle_pos, self.y, self.handle_width, self.height)

	def _value_to_pos(self, value):
		pos_range = self.width - self.handle_width
		return int(pos_range * (value - self.min_value) / self.value_range)

	def _pos_to_value(self, pos):
		pos_range = self.width - self.handle_width
		return int(pos * self.value_range / pos_range + self.min_value)

	def draw(self, surface):
		mousePos = pygame.mouse.get_pos()

		#if mouse is on handle and is pressed
		if self.handle_rect.collidepoint(mousePos) and pygame.mouse.get_pressed()[0] == 1:
			if self.x <= mousePos[0] <= self.x + self.width and self.y <= mousePos[1] <= self.y + self.height:
				self.handle_pos = min(max(mousePos[0] - self.x - self.handle_width // 2, 0), self.width - self.handle_width)
				self.value = self._pos_to_value(self.handle_pos)

		self.handle_rect = pygame.Rect(self.x + self.handle_pos, self.y, self.handle_width, self.height)

		# Draw the bar
		bar_rect = pygame.Rect(self.x, self.y + self.height // 2 - 1, self.width, 2)
		pygame.draw.rect(surface, self.bar_color, bar_rect)

		# Draw the handle
		handle_rect = pygame.Rect(self.x + self.handle_pos, self.y, self.handle_width, self.height)
		pygame.draw.rect(surface, self.handle_color, self.handle_rect)
