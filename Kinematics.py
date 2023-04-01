from ProjectConstants import *
import math


class Kinematics:
	groundHeight = SCREEN_HEIGHT - 150
	massRadius = 20

	def __init__(self, centerX, centerY, initialVelocity, angle):
		self.originalCenterX = centerX
		self.originalCenterY = centerY
		self.angle = angle
		self.initialVelocity = initialVelocity
		self.initialXVelocity = math.cos(math.radians(angle)) * self.initialVelocity
		self.initialYVelocity = -math.sin(math.radians(angle)) * self.initialVelocity
		self.currentYVelocity = self.initialYVelocity
		self.currentCenterX = centerX
		self.currentCenterY = centerY
		self.ifAnimating = False
		self.ifDoneAnimating = False

	def set_ifAnimating(self, ifAnimating):
		self.ifAnimating = ifAnimating

	def get_ifAnimating(self):
		return self.ifAnimating

	def get_ifDoneAnimating(self):
		return self.ifDoneAnimating

	def set_pos(self, centerX, centerY):
		self.originalCenterX = centerX
		self.originalCenterY = centerY
		self.currentCenterX = self.originalCenterX
		self.currentCenterY = self.originalCenterY
		self.ifDoneAnimating = False

	def recalculate_velocities(self):
		self.initialXVelocity = math.cos(math.radians(self.angle)) * self.initialVelocity
		self.initialYVelocity = -math.sin(math.radians(self.angle)) * self.initialVelocity
		self.currentYVelocity = self.initialYVelocity

	def set_angle(self, angle):
		self.angle = angle
		self.recalculate_velocities()

	def set_initial_velocity(self, initialVelocity):
		self.initialVelocity = initialVelocity
		self.recalculate_velocities()

	def calculate_time(self):
		#for equation y = y0 + vt + 1/2 * at^2 => 1/2 * at^2 + vt + height - ground_height + radius = 0
		a = GRAVITY / 2
		b = self.initialYVelocity
		c = self.originalCenterY - Kinematics.groundHeight + Kinematics.massRadius

		discriminant = math.pow(b, 2) - 4 * a * c
		if discriminant < 0:
			return None
		elif discriminant == 0:
			return -b / (2 * a)
		else:
			#only positive time
			root = (-b + math.sqrt(discriminant)) / (2 * a)
			return root

	def calculate_horizontal_distance(self):
		return self.initialXVelocity * self.calculate_time()

	def calculate_vertical_distance(self):
		return self.originalCenterY + self.initialYVelocity * self.calculate_time() + 1 / 2 * GRAVITY * math.pow(self.calculate_time(), 2)

	def draw_static(self, surface):
		pygame.draw.circle(surface, objectsColor, (self.currentCenterX, self.currentCenterY), Kinematics.massRadius)

		if not self.ifAnimating and not self.ifDoneAnimating:
			arrowLayerPos = (self.currentCenterX - 100, self.currentCenterY - 100)
			arrowLayer = pygame.Surface((200, 200)).convert_alpha()
			arrowLayer.fill((0, 0, 0, 0))

			arrowWidth = self.initialVelocity / 100 * 70

			pygame.draw.rect(arrowLayer, objectsColor, (100 + Kinematics.massRadius + 10, 97, arrowWidth, 6))

			rotatedSurface, center = rotate_surface(arrowLayer, self.angle, self.currentCenterX, self.currentCenterY)

			surface.blit(rotatedSurface, center)

	def next_launch_frame(self, playBackSpeed):
		self.currentCenterX += self.initialXVelocity * playBackSpeed / FPS
		self.currentYVelocity += GRAVITY * playBackSpeed / FPS
		self.currentCenterY += self.currentYVelocity * playBackSpeed / FPS

		# print(self.calculate_vertical_distance())
		# print(self.currentCenterY)
		#
		# print(self.calculate_horizontal_distance())
		# print(self.currentCenterX)

		if self.currentCenterY >= self.calculate_vertical_distance():
			self.ifAnimating = False
			self.ifDoneAnimating = True

			self.currentCenterX = self.calculate_horizontal_distance() + self.originalCenterX
			self.currentCenterY = self.calculate_vertical_distance()
