from ProjectConstants import *
import math


class MassMath:
	def __init__(self, centerX, centerY, initialVelocity, angle):
		self.centerX = centerX
		self.centerY = centerY
		self.angle = angle
		self.initialVelocity = initialVelocity
		self.initialXVelocity = math.cos(math.radians(angle)) * self.initialVelocity
		self.initialYVelocity = math.sin(math.radians(angle)) * self.initialVelocity

	def change_pos(self, centerX, centerY):
		self.centerX = centerX
		self.centerY = centerY

	def recalculate_velocities(self):
		self.initialXVelocity = math.cos(math.radians(self.angle)) * self.initialVelocity
		self.initialYVelocity = math.sin(math.radians(self.angle)) * self.initialVelocity

	def set_angle(self, angle):
		self.angle = angle
		self.recalculate_velocities()

	def set_initial_velocity(self, initialVelocity):
		self.initialVelocity = initialVelocity
		self.recalculate_velocities()

	def calculate_time(self):
		#for equation y = y0 + vt + at^2 => at^2 + vt + height - screen_height = 0
		a = gravity
		b = self.initialYVelocity
		c = self.centerY - SCREEN_HEIGHT

		discriminant = b ^ 2 - 4 * a * c
		if discriminant < 0:
			return None
		elif discriminant == 0:
			return -b / (2 * a)
		else:
			#only positive time
			root = (-b - math.sqrt(discriminant)) / (2 * a)
			return root

	def calculate_horizontal_distance(self):
		return self.initialXVelocity * self.calculate_time()

	def draw_static(self, surface):
		pygame.draw.circle(surface, objectsColor, (self.centerX, self.centerY), massRadius)

	def draw_animation(self, surface):
		while self.centerX < self.calculate_horizontal_distance():
			print("pause")
