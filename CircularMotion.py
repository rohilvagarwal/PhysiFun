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
		self.horizontalVelocity = None
		self.verticalVelocity = None
		self.playBackSpeed = 1

	def set_playBackSpeed(self, playBackSpeed):
		self.playBackSpeed = playBackSpeed

	def calculate_horizontal_and_vertical_velocity(self):
		self.verticalVelocity = math.cos(math.radians(self.angle)) * self.tangentialVelocity
		self.horizontalVelocity = -math.sin(math.radians(self.angle)) * self.tangentialVelocity

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
		self.angle += (self.rotationalVelocity * 180 / math.pi) * self.playBackSpeed / FPS
		self.angle = self.angle % 360

	def draw_static(self, screen, scale, maxTangentialVelocity):
		#Scale bar
		#draw scale bar (1 pixel is scale meters)
		pygame.draw.rect(screen, objectsColor, (SCREEN_WIDTH - 25 - 100 - 4, 75 + 20 - 2, 100, 4))  #bar
		pygame.draw.rect(screen, objectsColor, (SCREEN_WIDTH - 25 - 100 - 4 - 4, 75 + 20 - 10, 4, 20))  #left edge
		pygame.draw.rect(screen, objectsColor, (SCREEN_WIDTH - 25 - 4, 75 + 20 - 10, 4, 20))  #right edge
		draw_text_center(screen, SCREEN_WIDTH - 25 - 50 - 4, 75 + 20 + 10, 15, str("{:.0f}".format(100 * scale)) + "m")
		draw_text_right(screen, SCREEN_WIDTH - 25, 12, 15, "*Each Pixel is " + str(scale) + "m")

		#stats
		draw_text_right(screen, SCREEN_WIDTH - 130, 140, 20, "Speed:")
		draw_text_left(screen, SCREEN_WIDTH - 120, 140, 20, str(self.playBackSpeed) + "x")

		#ground
		pygame.draw.rect(screen, objectsColor, (0, CircularMotion.groundHeight, SCREEN_WIDTH, 10))

		#screen segments
		pygame.draw.rect(screen, objectsColor, (self.pivotX * 2 - 5, 0, 10, CircularMotion.groundHeight))

		#titles
		draw_text_center(screen, self.pivotX, 30, 30, "Circular Motion")
		draw_text_center(screen, SCREEN_WIDTH - self.pivotX - 50, 30, 30, "Instantaneous Vel.")

		#pivot
		pygame.draw.circle(screen, objectsColor, (self.pivotX, self.pivotY), CircularMotion.pivotRadius)

		#Mass and Acceleration Arrow
		arrowAndMassLayer = pygame.Surface((500, 500)).convert_alpha()  #center is on pivot point
		arrowAndMassLayer.fill((0, 0, 0, 0))

		pygame.draw.circle(arrowAndMassLayer, objectsColor, (250 + self.radius / scale, 250), CircularMotion.massRadius)  #radius max 200

		pygame.draw.rect(arrowAndMassLayer, objectsColor, (
			250 + CircularMotion.pivotRadius + 10 + 10, 247,
			self.radius / scale - CircularMotion.massRadius - CircularMotion.pivotRadius - 10 - 10 - 10, 6))
		pygame.draw.polygon(arrowAndMassLayer, objectsColor, ((250 + CircularMotion.pivotRadius + 10 + 10, 240),
															  (250 + CircularMotion.pivotRadius + 10, 250),
															  (250 + CircularMotion.pivotRadius + 10 + 10, 260)))

		rotatedSurface, center = rotate_surface(arrowAndMassLayer, self.angle, self.pivotX, self.pivotY)

		screen.blit(rotatedSurface, center)

		#Velocities Visualization
		self.calculate_horizontal_and_vertical_velocity()

		pygame.draw.circle(screen, objectsColor, (SCREEN_WIDTH - self.pivotX, self.pivotY), CircularMotion.pivotRadius)

		horizontalVelocityArrowLength = self.horizontalVelocity / maxTangentialVelocity * 200
		verticalVelocityArrowLength = self.verticalVelocity / maxTangentialVelocity * 200

		if horizontalVelocityArrowLength > 0:
			pygame.draw.rect(screen, objectsColor,
							 (SCREEN_WIDTH - self.pivotX + CircularMotion.pivotRadius + 10, self.pivotY - 3, horizontalVelocityArrowLength, 6))
			pygame.draw.polygon(screen, objectsColor,
								((SCREEN_WIDTH - self.pivotX + CircularMotion.pivotRadius + 10 + horizontalVelocityArrowLength, self.pivotY - 10),
								 (SCREEN_WIDTH - self.pivotX + CircularMotion.pivotRadius + 10 + horizontalVelocityArrowLength + 10, self.pivotY),
								 (SCREEN_WIDTH - self.pivotX + CircularMotion.pivotRadius + 10 + horizontalVelocityArrowLength, self.pivotY + 10)))
		# pygame.draw.polygon(screen, objectsColor,
		# 					((SCREEN_WIDTH - self.pivotX - CircularMotion.pivotRadius - 10, self.pivotY - 10),
		# 					 (SCREEN_WIDTH - self.pivotX - CircularMotion.pivotRadius - 10 - 10, self.pivotY),
		# 					 (SCREEN_WIDTH - self.pivotX - CircularMotion.pivotRadius - 10, self.pivotY + 10)))

		elif horizontalVelocityArrowLength < 0:
			pygame.draw.rect(screen, objectsColor, (
				SCREEN_WIDTH - self.pivotX - CircularMotion.pivotRadius - 10 + horizontalVelocityArrowLength, self.pivotY - 3,
				-horizontalVelocityArrowLength, 6))

			pygame.draw.polygon(screen, objectsColor,
								((SCREEN_WIDTH - self.pivotX - CircularMotion.pivotRadius - 10 + horizontalVelocityArrowLength, self.pivotY - 10),
								 (SCREEN_WIDTH - self.pivotX - CircularMotion.pivotRadius - 10 + horizontalVelocityArrowLength - 10, self.pivotY),
								 (SCREEN_WIDTH - self.pivotX - CircularMotion.pivotRadius - 10 + horizontalVelocityArrowLength, self.pivotY + 10)))

		if verticalVelocityArrowLength > 0:
			pygame.draw.rect(screen, objectsColor, (
				SCREEN_WIDTH - self.pivotX - 3, self.pivotY - CircularMotion.pivotRadius - 10 - verticalVelocityArrowLength, 6,
				verticalVelocityArrowLength))
			pygame.draw.polygon(screen, objectsColor,
								((SCREEN_WIDTH - self.pivotX - 10, self.pivotY - CircularMotion.pivotRadius - 10 - verticalVelocityArrowLength),
								 (SCREEN_WIDTH - self.pivotX, self.pivotY - CircularMotion.pivotRadius - 10 - verticalVelocityArrowLength - 10),
								 (SCREEN_WIDTH - self.pivotX + 10, self.pivotY - CircularMotion.pivotRadius - 10 - verticalVelocityArrowLength)))

		elif verticalVelocityArrowLength < 0:
			pygame.draw.rect(screen, objectsColor, (
				SCREEN_WIDTH - self.pivotX - 3, self.pivotY + CircularMotion.pivotRadius + 10, 6,
				-verticalVelocityArrowLength))
			pygame.draw.polygon(screen, objectsColor,
								((SCREEN_WIDTH - self.pivotX - 10, self.pivotY + CircularMotion.pivotRadius + 10 - verticalVelocityArrowLength),
								 (SCREEN_WIDTH - self.pivotX, self.pivotY + CircularMotion.pivotRadius + 10 - verticalVelocityArrowLength + 10),
								 (SCREEN_WIDTH - self.pivotX + 10, self.pivotY + CircularMotion.pivotRadius + 10 - verticalVelocityArrowLength)))

		#Stats
		#draw_text_right(screen, self.pivotX - 5, CircularMotion.groundHeight - 20, 20, "Centripetal Acceleration:")
		#draw_text_left(screen, self.pivotX + 5, CircularMotion.groundHeight - 20, 20, str("{:.1f}".format(self.centripetalAcceleration)) + " m/s^2")
		# draw_superscript(screen, draw_text_left(screen, self.pivotX + 5, CircularMotion.groundHeight - 20, 20,
		# 										str("{:.1f}".format(self.centripetalAcceleration)) + " m/s"), "2")
		draw_left_with_superscript(screen, 60, CircularMotion.groundHeight - 20, 20,
								   "Centripetal Acceleration: " + str("{:.2f}".format(self.centripetalAcceleration)) + " m/s^2")

	@staticmethod
	def calculate_rotationalVelocity_test(tangentialVelocity, radius):
		return tangentialVelocity / radius

	@staticmethod
	def calculate_tangentialVelocity_test(rotationalVelocity, radius):
		return rotationalVelocity * radius
