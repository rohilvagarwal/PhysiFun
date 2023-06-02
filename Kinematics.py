from ProjectConstants import *
import math


class Kinematics:
	groundHeight = SCREEN_HEIGHT - 150
	massRadius = 20

	def __init__(self, centerX, centerY, initialVelocity, angle):
		self.state = "default"  #default, animating, paused, doneAnimating
		self.originalCenterX = centerX
		self.originalCenterY = centerY
		self.angle = angle  #degrees
		self.initialVelocity = initialVelocity
		self.initialXVelocity = math.cos(math.radians(angle)) * self.initialVelocity
		self.initialYVelocity = -math.sin(math.radians(angle)) * self.initialVelocity
		self.currentYVelocity = self.initialYVelocity
		self.currentCenterX = centerX
		self.currentCenterY = centerY
		self.arrowWidth = 0
		self.playBackSpeed = 1
		self.currentTime = 0.000

	def set_state(self, state):
		self.state = state

	def get_state(self):
		return self.state

	def set_pos(self, centerX, centerY):
		self.originalCenterX = centerX
		self.originalCenterY = centerY
		self.currentCenterX = self.originalCenterX
		self.currentCenterY = self.originalCenterY
		self.state = "default"
		self.arrowWidth = 0
		#self.framesPast = 0
		self.currentTime = 0.000

	#self.playBackSpeed = 1

	def set_playbackSpeed(self, playbackSpeed):
		self.playBackSpeed = playbackSpeed

	def get_playbackSpeed(self):
		return self.playBackSpeed

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

	def calculate_time_till_ground(self):
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

	def calculate_current_time_per_frame(self):
		self.currentTime += 1 / FPS * self.playBackSpeed

	def calculate_time_max_height(self):
		max_height_time = -self.initialYVelocity / GRAVITY
		if max_height_time <= 0:
			return 0
		else:
			return max_height_time

	def calculate_vertical_position(self, time):
		return Kinematics.groundHeight - self.originalCenterY - Kinematics.massRadius + -self.initialYVelocity * time + 1 / 2 * -GRAVITY * math.pow(
			time, 2)

	def calculate_total_horizontal_distance(self):
		return self.initialXVelocity * self.calculate_time_till_ground()

	def calculate_total_vertical_distance(self):
		return self.originalCenterY + self.initialYVelocity * self.calculate_time_till_ground() + 1 / 2 * GRAVITY * math.pow(
			self.calculate_time_till_ground(), 2)

	def next_launch_frame(self):
		#self.framesPast += 1
		self.calculate_current_time_per_frame()
		self.currentCenterX += self.initialXVelocity * self.playBackSpeed / FPS
		self.currentYVelocity += GRAVITY * self.playBackSpeed / FPS
		self.currentCenterY += self.currentYVelocity * self.playBackSpeed / FPS

		if self.currentCenterY >= self.calculate_total_vertical_distance():
			self.set_state("doneAnimating")

			self.currentCenterX = self.calculate_total_horizontal_distance() + self.originalCenterX
			self.currentCenterY = self.calculate_total_vertical_distance()

	def draw_static(self, screen):
		#ground
		pygame.draw.rect(screen, objectsColor, (0, Kinematics.groundHeight, SCREEN_WIDTH, 10))

		#draw scale bar (1 pixel is 1m)
		pygame.draw.rect(screen, objectsColor, (SCREEN_WIDTH - 25 - 100 - 4, 75 + 20 - 2, 100, 4))  #bar
		pygame.draw.rect(screen, objectsColor, (SCREEN_WIDTH - 25 - 100 - 4 - 4, 75 + 20 - 10, 4, 20))  #left edge
		pygame.draw.rect(screen, objectsColor, (SCREEN_WIDTH - 25 - 4, 75 + 20 - 10, 4, 20))  #right edge
		draw_text_center(screen, SCREEN_WIDTH - 25 - 50 - 4, 75 + 20 + 10, 15, "100m")
		draw_text_right(screen, SCREEN_WIDTH - 25, 12, 15, "*Each Pixel is 1m")

		#mass
		pygame.draw.circle(screen, objectsColor, (self.currentCenterX, self.currentCenterY), Kinematics.massRadius)

		if self.state == "default":
			arrowLayer = pygame.Surface((200, 200)).convert_alpha()  #center is on center of mass
			arrowLayer.fill((0, 0, 0, 0))

			arrowLength = self.initialVelocity / 100 * 50

			pygame.draw.rect(arrowLayer, objectsColor, (100 + Kinematics.massRadius + 10, 97, arrowLength, 6))
			pygame.draw.polygon(arrowLayer, objectsColor, ((100 + Kinematics.massRadius + 10 + arrowLength, 90),
														   (100 + Kinematics.massRadius + 10 + arrowLength + 10, 100),
														   (100 + Kinematics.massRadius + 10 + arrowLength, 110)))

			rotatedSurface, center = rotate_surface(arrowLayer, self.angle, self.currentCenterX, self.currentCenterY)

			screen.blit(rotatedSurface, center)

		if self.calculate_total_horizontal_distance() > SCREEN_WIDTH - self.originalCenterX:
			draw_text_right(screen, SCREEN_WIDTH - 10, 400, 10, "The ball will")
			draw_text_right(screen, SCREEN_WIDTH - 10, 412, 10, "exceed the edge!")

		if not self.state == "doneAnimating":
			draw_text_right(screen, SCREEN_WIDTH - 130, 140, 20, "Speed:")
			draw_text_left(screen, SCREEN_WIDTH - 120, 140, 20, str(self.playBackSpeed) + "x")

			draw_text_right(screen, SCREEN_WIDTH - 130, 170, 20, "Time:")
			draw_text_left(screen, SCREEN_WIDTH - 120, 170, 20, str("{:.3f}".format(self.currentTime)) + " s")

			draw_text_right(screen, SCREEN_WIDTH - 130, 200, 20, "Max Height:")
			draw_text_left(screen, SCREEN_WIDTH - 120, 200, 20, "?")

		if self.state == "doneAnimating":
			draw_text_right(screen, SCREEN_WIDTH - 130, 140, 20, "Speed:")
			draw_text_left(screen, SCREEN_WIDTH - 120, 140, 20, str(self.playBackSpeed) + "x")
			
			draw_text_right(screen, SCREEN_WIDTH - 130, 170, 20, "Time:")
			draw_text_left(screen, SCREEN_WIDTH - 120, 170, 20, str("{:.3f}".format(self.calculate_time_till_ground())) + " s")

			draw_text_right(screen, SCREEN_WIDTH - 130, 200, 20, "Max Height:")
			draw_text_left(screen, SCREEN_WIDTH - 120, 200, 20,
						   str("{:.3f}".format(self.calculate_vertical_position(self.calculate_time_max_height()))) + " m")

			if self.arrowWidth < self.calculate_total_horizontal_distance() - Kinematics.massRadius - 20:
				self.arrowWidth += 800 / FPS
			else:
				self.arrowWidth = self.calculate_total_horizontal_distance() - Kinematics.massRadius - 20
				pygame.draw.polygon(screen, objectsColor, ((self.currentCenterX - Kinematics.massRadius - 20, self.currentCenterY - 10),
														   (self.currentCenterX - Kinematics.massRadius - 20 + 10, self.currentCenterY),
														   (self.currentCenterX - Kinematics.massRadius - 20, self.currentCenterY + 10)))

				draw_text_center(screen, self.calculate_total_horizontal_distance() / 2 + self.originalCenterX,
								 Kinematics.groundHeight - Kinematics.massRadius - 30, 20,
								 str("{:.3f}".format(self.calculate_total_horizontal_distance())) + " m")

			pygame.draw.rect(screen, objectsColor, (self.originalCenterX, Kinematics.groundHeight - Kinematics.massRadius - 3, self.arrowWidth, 6))
