import pygame.draw

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
		self.arrowWidth = 0
		self.framesPast = 0
		self.playBackSpeed = 1

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
		self.arrowWidth = 0
		self.framesPast = 0
		self.playBackSpeed = 1

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
		return self.initialXVelocity * self.calculate_time()

	def calculate_total_vertical_distance(self):
		return self.originalCenterY + self.initialYVelocity * self.calculate_time() + 1 / 2 * GRAVITY * math.pow(self.calculate_time(), 2)

	def draw_static(self, surface):
		pygame.draw.circle(surface, objectsColor, (self.currentCenterX, self.currentCenterY), Kinematics.massRadius)

		if not self.ifAnimating and not self.ifDoneAnimating:
			arrowLayer = pygame.Surface((200, 200)).convert_alpha()
			arrowLayer.fill((0, 0, 0, 0))

			arrowWidth = self.initialVelocity / 100 * 50

			pygame.draw.rect(arrowLayer, objectsColor, (100 + Kinematics.massRadius + 10, 97, arrowWidth, 6))
			pygame.draw.polygon(arrowLayer, objectsColor, ((100 + Kinematics.massRadius + 10 + arrowWidth, 90),
														   (100 + Kinematics.massRadius + 10 + arrowWidth + 10, 100),
														   (100 + Kinematics.massRadius + 10 + arrowWidth, 110)))

			rotatedSurface, center = rotate_surface(arrowLayer, self.angle, self.currentCenterX, self.currentCenterY)

			surface.blit(rotatedSurface, center)

		if not self.ifDoneAnimating:
			valueFont = pygame.font.SysFont("jost700", 20)
			timeText = valueFont.render("Time: " + str(round((self.framesPast * 1 / FPS) * self.playBackSpeed, 3)) + " s", True, textColor)

			surface.blit(timeText, (SCREEN_WIDTH - 220, 300))

	def next_launch_frame(self, playBackSpeed):
		self.playBackSpeed = playBackSpeed
		self.framesPast += 1
		self.currentCenterX += self.initialXVelocity * playBackSpeed / FPS
		self.currentYVelocity += GRAVITY * playBackSpeed / FPS
		self.currentCenterY += self.currentYVelocity * playBackSpeed / FPS

		if self.currentCenterY >= self.calculate_total_vertical_distance():
			self.ifAnimating = False
			self.ifDoneAnimating = True

			self.currentCenterX = self.calculate_total_horizontal_distance() + self.originalCenterX
			self.currentCenterY = self.calculate_total_vertical_distance()

	def after_animation(self, surface):
		if self.ifDoneAnimating:
			valueFont = pygame.font.SysFont("jost700", 20)
			timeText = valueFont.render("Time: " + str(round(self.calculate_time(), 3)) + " s", True, textColor)
			surface.blit(timeText, (SCREEN_WIDTH - 220, 300))

			heightText = valueFont.render("Max Height: " + str(round(self.calculate_vertical_position(self.calculate_time_max_height()), 2)) + " m",
										  True, textColor)
			surface.blit(heightText, (SCREEN_WIDTH - 220, 330))

			if self.arrowWidth < self.calculate_total_horizontal_distance() - Kinematics.massRadius - 20:
				self.arrowWidth += 500 / FPS
			else:
				self.arrowWidth = self.calculate_total_horizontal_distance() - Kinematics.massRadius - 20
				pygame.draw.polygon(surface, objectsColor, ((self.currentCenterX - Kinematics.massRadius - 20, self.currentCenterY - 10),
															(self.currentCenterX - Kinematics.massRadius - 20 + 10, self.currentCenterY),
															(self.currentCenterX - Kinematics.massRadius - 20, self.currentCenterY + 10)))

				distanceText = valueFont.render(str(round(self.calculate_total_horizontal_distance(), 3)) + " m", True, textColor)
				textPosition = distanceText.get_rect(center=(
					self.calculate_total_horizontal_distance() / 2 + self.originalCenterX, Kinematics.groundHeight - Kinematics.massRadius - 3 - 10))
				surface.blit(distanceText, textPosition)

			pygame.draw.rect(surface, objectsColor, (self.originalCenterX, Kinematics.groundHeight - Kinematics.massRadius - 3, self.arrowWidth, 6))
