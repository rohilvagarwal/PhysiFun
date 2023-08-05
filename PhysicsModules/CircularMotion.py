from ProjectConstants import *
import math
from UIElements.Button import Button
from UIElements.SliderBar import SliderBar


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

		#general buttons
		self.defaultButton = Button(centerX=SCREEN_WIDTH - 125, centerY=SCREEN_HEIGHT - 95, width=200, height=50, textSize=30, borderSize=10,
									text="Default")
		self.pauseButton = Button(centerX=SCREEN_WIDTH - 125, centerY=SCREEN_HEIGHT - 40, width=200, height=50, textSize=30, borderSize=10,
								  text="Pause")
		self.resumeButton = Button(centerX=SCREEN_WIDTH - 125, centerY=SCREEN_HEIGHT - 40, width=200, height=50, textSize=30, borderSize=10,
								   text="Resume")
		self.resetButton = Button(centerX=SCREEN_WIDTH - 125, centerY=SCREEN_HEIGHT - 95, width=200, height=50, textSize=30, borderSize=10,
								  text="Reset")

		#interactive elements
		self.minRotationalVelocity = -4 * math.pi
		self.maxRotationalVelocity = 4 * math.pi
		self.rotationalVelocityBar = SliderBar(25, SCREEN_HEIGHT - 50, 200, 20, self.minRotationalVelocity, self.maxRotationalVelocity, math.pi,
											   "Rotational Vel. (rad/s)", 2)
		minTangentialVelocity = -4 * math.pi * 20
		self.maxTangentialVelocity = 4 * math.pi * 20
		self.tangentialVelocityBar = SliderBar(290, SCREEN_HEIGHT - 50, 200, 20, minTangentialVelocity, self.maxTangentialVelocity, math.pi * 10,
											   "Tangential Vel. (m/s)", 2)
		self.radiusBar = SliderBar(555, SCREEN_HEIGHT - 50, 200, 20, 5, 20, 10, "Radius (m)", 1)

		self.tangentialVelocityBar.set_lowerBoundValue(self.minRotationalVelocity * self.get_radius())
		self.tangentialVelocityBar.set_upperBoundValue(self.maxRotationalVelocity * self.get_radius())

		self.minusPi = Button(centerX=35, centerY=SCREEN_HEIGHT - 110, width=40, height=40, textSize=20, borderSize=10, text="-π")
		self.minusPiOverTwo = Button(centerX=80, centerY=SCREEN_HEIGHT - 110, width=40, height=40, textSize=10, borderSize=10, text="-π/2")
		self.zeroPi = Button(centerX=125, centerY=SCREEN_HEIGHT - 110, width=40, height=40, textSize=20, borderSize=10, text="0")
		self.plusPiOverTwo = Button(centerX=170, centerY=SCREEN_HEIGHT - 110, width=40, height=40, textSize=10, borderSize=10, text="+π/2")
		self.plusPi = Button(centerX=215, centerY=SCREEN_HEIGHT - 110, width=40, height=40, textSize=20, borderSize=10, text="+π")

		self.oneXSpeed = Button(centerX=460, centerY=SCREEN_HEIGHT - 110, width=40, height=40, textSize=20, borderSize=10, text="1x")
		self.halfXSpeed = Button(centerX=510, centerY=SCREEN_HEIGHT - 110, width=40, height=40, textSize=12, borderSize=10, text="0.5x")
		self.fourthXSpeed = Button(centerX=560, centerY=SCREEN_HEIGHT - 110, width=40, height=40, textSize=10, borderSize=10, text="0.25x")
		self.tenthXSpeed = Button(centerX=610, centerY=SCREEN_HEIGHT - 110, width=40, height=40, textSize=12, borderSize=10, text="0.1x")

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

	def draw_static(self, screen, scale):
		#interactive elements
		draw_text_center(screen, 355, SCREEN_HEIGHT - 110, 20, "Playback Speed:")
		if self.oneXSpeed.draw_and_check_click(screen):
			self.set_playBackSpeed(1)
		if self.halfXSpeed.draw_and_check_click(screen):
			self.set_playBackSpeed(0.5)
		if self.fourthXSpeed.draw_and_check_click(screen):
			self.set_playBackSpeed(0.25)
		if self.tenthXSpeed.draw_and_check_click(screen):
			self.set_playBackSpeed(0.1)

		if self.defaultButton.draw_and_check_click(screen):
			self.rotationalVelocityBar.set_value(math.pi)
			self.tangentialVelocityBar.set_value(math.pi * 10)
			self.radiusBar.set_value(10)
			self.set_angle(0)
			self.set_playBackSpeed(1)

			self.set_radius(10)
			self.set_rotationalVelocity(math.pi)
			self.set_tangentialVelocity(math.pi * 10)

		if self.minusPi.draw_and_check_click(screen):
			if self.get_rotationalVelocity() - math.pi < self.minRotationalVelocity:
				self.rotationalVelocityBar.set_value(self.minRotationalVelocity)
				self.set_rotationalVelocity(self.minRotationalVelocity)
				self.tangentialVelocityBar.set_value(self.get_tangentialVelocity())
			else:
				self.rotationalVelocityBar.set_value(self.get_rotationalVelocity() - math.pi)
				self.set_rotationalVelocity(self.get_rotationalVelocity() - math.pi)
				self.tangentialVelocityBar.set_value(self.get_tangentialVelocity())

		if self.minusPiOverTwo.draw_and_check_click(screen):
			if self.get_rotationalVelocity() - math.pi / 2 < self.minRotationalVelocity:
				self.rotationalVelocityBar.set_value(self.minRotationalVelocity)
				self.set_rotationalVelocity(self.minRotationalVelocity)
				self.tangentialVelocityBar.set_value(self.get_tangentialVelocity())
			else:
				self.rotationalVelocityBar.set_value(self.get_rotationalVelocity() - math.pi / 2)
				self.set_rotationalVelocity(self.get_rotationalVelocity() - math.pi / 2)
				self.tangentialVelocityBar.set_value(self.get_tangentialVelocity())

		if self.zeroPi.draw_and_check_click(screen):
			self.rotationalVelocityBar.set_value(0)
			self.set_rotationalVelocity(0)
			self.tangentialVelocityBar.set_value(self.get_tangentialVelocity())

		if self.plusPiOverTwo.draw_and_check_click(screen):
			if self.get_rotationalVelocity() + math.pi / 2 > self.maxRotationalVelocity:
				self.rotationalVelocityBar.set_value(self.maxRotationalVelocity)
				self.set_rotationalVelocity(self.maxRotationalVelocity)
				self.tangentialVelocityBar.set_value(self.get_tangentialVelocity())
			else:
				self.rotationalVelocityBar.set_value(self.get_rotationalVelocity() + math.pi / 2)
				self.set_rotationalVelocity(self.get_rotationalVelocity() + math.pi / 2)
				self.tangentialVelocityBar.set_value(self.get_tangentialVelocity())

		if self.plusPi.draw_and_check_click(screen):
			if self.get_rotationalVelocity() + math.pi > self.maxRotationalVelocity:
				self.rotationalVelocityBar.set_value(self.maxRotationalVelocity)
				self.set_rotationalVelocity(self.maxRotationalVelocity)
				self.tangentialVelocityBar.set_value(self.get_tangentialVelocity())
			else:
				self.rotationalVelocityBar.set_value(self.get_rotationalVelocity() + math.pi)
				self.set_rotationalVelocity(self.get_rotationalVelocity() + math.pi)
				self.tangentialVelocityBar.set_value(self.get_tangentialVelocity())

		self.rotationalVelocityBar.draw(screen)
		self.tangentialVelocityBar.draw(screen)
		self.radiusBar.draw(screen)

		#if not self.get_rotationalVelocity() == self.rotationalVelocityBar.get_value():
		if self.rotationalVelocityBar.get_handleSelected():
			self.set_rotationalVelocity(self.rotationalVelocityBar.get_value())
			self.tangentialVelocityBar.set_value(self.get_tangentialVelocity())

		#if not self.get_tangentialVelocity() == self.tangentialVelocityBar.get_value():
		if self.tangentialVelocityBar.get_handleSelected():
			self.set_tangentialVelocity(self.tangentialVelocityBar.get_value())
			self.rotationalVelocityBar.set_value(self.get_rotationalVelocity())

		#if not self.get_radius() == self.radiusBar.get_value():
		if self.radiusBar.get_handleSelected():
			self.set_radius(self.radiusBar.get_value())
			self.set_rotationalVelocity(self.rotationalVelocityBar.get_value())
			self.tangentialVelocityBar.set_value(self.get_tangentialVelocity())

			self.tangentialVelocityBar.set_lowerBoundValue(self.minRotationalVelocity * self.get_radius())
			self.tangentialVelocityBar.set_upperBoundValue(self.maxRotationalVelocity * self.get_radius())

		if self.get_state() == "animating":
			self.next_frame()

			if self.pauseButton.draw_and_check_click(screen):
				self.set_state("paused")

		elif self.get_state() == "paused":
			if self.resumeButton.draw_and_check_click(screen):
				self.set_state("animating")

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

		horizontalVelocityArrowLength = self.horizontalVelocity / self.maxTangentialVelocity * 200
		verticalVelocityArrowLength = self.verticalVelocity / self.maxTangentialVelocity * 200

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
