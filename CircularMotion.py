from ProjectConstants import *
import math


class CircularMotion:
	groundHeight = SCREEN_HEIGHT - 150
	pivotRadius = 5
	massRadius = 20

	def __init__(self, pivotX, pivotY, radius):
		self.state = "animating"  #animating, paused
		self.pivotX = pivotX
		self.pivotY = pivotY
		self.radius = radius
		self.rotationalVelocity = math.pi  #rad/s
		self.tangentialVelocity = self.rotationalVelocity * self.radius
		self.centripetalAcceleration = math.pow(self.tangentialVelocity, 2) / self.radius
		self.angle = 0

	def set_state(self, state):
		self.state = state

	def get_state(self):
		return self.state

	def set_angle(self, angle):
		self.angle = angle

	def set_radius(self, radius):
		self.radius = radius
		self.recalculate_centripetalAcceleration()

	def get_radius(self):
		return self.radius

	def set_rotationalVelocity(self, rotationalVelocity):
		self.rotationalVelocity = rotationalVelocity
		self.tangentialVelocity = self.rotationalVelocity * self.radius
		self.recalculate_centripetalAcceleration()

	def get_rotationalVelocity(self):
		return self.rotationalVelocity

	def set_tangentialVelocity(self, tangentialVelocity):
		self.tangentialVelocity = tangentialVelocity
		self.rotationalVelocity = self.tangentialVelocity / self.radius
		self.recalculate_centripetalAcceleration()

	def get_tangentialVelocity(self):
		return self.tangentialVelocity

	def recalculate_centripetalAcceleration(self):
		self.centripetalAcceleration = math.pow(self.tangentialVelocity, 2) / self.radius

	def next_frame(self):
		self.angle += (self.rotationalVelocity * 180 / math.pi) / FPS

	def draw_static(self, screen):
		#ground
		pygame.draw.rect(screen, objectsColor, (0, CircularMotion.groundHeight, SCREEN_WIDTH, 10))

		#pivot
		pygame.draw.circle(screen, objectsColor, (self.pivotX, self.pivotY), CircularMotion.pivotRadius)

		#Mass and Acceleration Arrow
		arrowAndMassLayer = pygame.Surface((500, 500)).convert_alpha()  #center is on pivot point
		arrowAndMassLayer.fill((0, 0, 0, 0))

		pygame.draw.circle(arrowAndMassLayer, objectsColor, (250 + self.radius, 250), CircularMotion.massRadius)  #radius max 200

		pygame.draw.rect(arrowAndMassLayer, objectsColor, (
			250 + CircularMotion.pivotRadius + 10 + 10, 247, self.radius - CircularMotion.massRadius - CircularMotion.pivotRadius - 10 - 10 - 10, 6))
		pygame.draw.polygon(arrowAndMassLayer, objectsColor, ((250 + CircularMotion.pivotRadius + 10 + 10, 240),
															  (250 + CircularMotion.pivotRadius + 10, 250),
															  (250 + CircularMotion.pivotRadius + 10 + 10, 260)))

		rotatedSurface, center = rotate_surface(arrowAndMassLayer, self.angle, self.pivotX, self.pivotY)

		screen.blit(rotatedSurface, center)

	@staticmethod
	def calculate_rotationalVelocity_test(tangentialVelocity, radius):
		return tangentialVelocity / radius

	@staticmethod
	def calculate_tangentialVelocity_test(rotationalVelocity, radius):
		return rotationalVelocity * radius
