from ProjectConstants import *


class SliderBar:
	def __init__(self, x, y, width, height, minValue, maxValue, defaultValue, title, decimalPlaces=0):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.minValue = minValue
		self.maxValue = maxValue
		self.valueRange = maxValue - minValue
		self.value = defaultValue
		self.handleWidth = height // 2
		self.handleSelected = False
		self.title = title
		self.decimalPlaces = decimalPlaces
		self.handlePos = self.value_to_pos(defaultValue)

	def get_value(self):
		return self.value

	def set_value(self, value):
		self.value = round(value, self.decimalPlaces)
		self.handlePos = self.value_to_pos(self.value)

	def value_to_pos(self, value):
		pos_range = self.width - self.handleWidth
		return round(pos_range * (value - self.minValue) / self.valueRange, self.decimalPlaces)

	def pos_to_value(self, pos):
		pos_range = self.width - self.handleWidth
		return round(pos * self.valueRange / pos_range + self.minValue, self.decimalPlaces)

	def draw(self, surface):
		mousePos = pygame.mouse.get_pos()

		#if self.x + self.handlePos - self.handleWidth // 2 <= mousePos[0] <= self.x + self.handlePos + self.handleWidth // 2:

		#if mouse is on handle and is pressed
		if pygame.mouse.get_pressed()[0] == 1:
			if self.x + self.handlePos - self.handleWidth // 2 <= mousePos[
				0] <= self.x + self.handlePos + self.handleWidth + self.handleWidth // 2 and self.y <= mousePos[1] <= self.y + self.height:
				self.handleSelected = True
				self.handlePos = min(max(mousePos[0] - self.x - self.handleWidth // 2, 0), self.width - self.handleWidth)
				self.value = self.pos_to_value(self.handlePos)
			elif self.handleSelected:
				self.handlePos = min(max(mousePos[0] - self.x - self.handleWidth // 2, 0), self.width - self.handleWidth)
				self.value = self.pos_to_value(self.handlePos)
		else:
			self.handleSelected = False

		self.draw_static(surface)

	def draw_static(self, surface):
		#draw bar
		bar_rect = pygame.Rect(self.x, self.y + self.height // 2 - 1, self.width, 2)
		pygame.draw.rect(surface, sliderBarColor, bar_rect)

		#write lower and upper bounds
		draw_text_left(surface, self.x, self.y + 3, 10, str(round(self.minValue, self.decimalPlaces)))
		draw_text_right(surface, self.x + self.width, self.y + 3, 10, str(round(self.maxValue, self.decimalPlaces)))

		#draw handle
		handle_rect = pygame.Rect(self.x + self.handlePos, self.y, self.handleWidth, self.height)
		pygame.draw.rect(surface, sliderBarHandleColor, handle_rect)

		#write value
		draw_text_top_left(surface, self.x, self.y + 15, 20, "{:.{}f}".format(self.value, self.decimalPlaces))

		#write title
		draw_text_top_left(surface, self.x, self.y - 35, 25, self.title)
