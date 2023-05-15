import pygame
import sys
from ProjectConstants import *
from Button import *
from SliderBar import *
from Kinematics import *
import time

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

#image imports
d4 = pygame.image.load('images/d4Logo.svg')
scaled_d4 = pygame.transform.scale(d4, (100, 100))

rojWidth = 300
roj = pygame.image.load('images/roj.png')
scaledRoj = pygame.transform.scale(roj, (rojWidth, rojWidth))

#game variables
GAME_OVER = False

#game states: menu, kinematics, about me
gameState = "menu"

#kinematics
kinematicsAngleBar = SliderBar(25, SCREEN_HEIGHT - 50, 200, 20, -90, 90, 0, "Angle (°)")
kinematicsHeightBar = SliderBar(250, SCREEN_HEIGHT - 50, 200, 20, 0, 500, 250, "Height (m)")
kinematicsVelocityBar = SliderBar(475, SCREEN_HEIGHT - 50, 200, 20, 0, 100, 50, "Initial Velocity (m/s)")
kinematicsMass = Kinematics(100, 500, 100, 0)
launchButton = Button(centerX=SCREEN_WIDTH - 125, centerY=SCREEN_HEIGHT - 30, width=200, height=50, textSize=30, borderSize=10, text="Launch")
defaultButton = Button(centerX=SCREEN_WIDTH - 125, centerY=SCREEN_HEIGHT - 85, width=200, height=50, textSize=30, borderSize=10, text="Default")
resetButton = Button(centerX=SCREEN_WIDTH - 125, centerY=SCREEN_HEIGHT - 50, width=200, height=50, textSize=30, borderSize=10, text="Reset")


def draw_text_center(centerX, centerY, textSize, text):
	font = pygame.font.SysFont("jost700", textSize)
	text = font.render(text, True, textColor)
	text_rect = text.get_rect(center=(centerX, centerY))
	screen.blit(text, text_rect)


def menu_button(centerY, text):
	return Button(centerX=200, centerY=centerY, width=200, height=50, textSize=30, borderSize=10, text=text)


def return_to_menu_button():
	global gameState

	menuButton = Button(centerX=SCREEN_WIDTH - 75, centerY=50, width=100, height=50, textSize=30, borderSize=10, text="Menu")

	if menuButton.draw(screen):
		gameState = "menu"


def draw_d4():
	screen.blit(scaled_d4, (10, 10))


def draw_menu():
	global gameState
	global GAME_OVER
	screen.fill(backgroundColor)
	draw_d4()

	#draw title
	draw_text_center(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 10, 70, "PhysicsStudy")
	draw_text_center(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 5, 30, "By Rohil Agarwal")

	kinematics = menu_button(SCREEN_HEIGHT / 4, "Kinematics")
	aboutMe = menu_button(2 * SCREEN_HEIGHT / 4, "About Me")
	exit = menu_button(3 * SCREEN_HEIGHT / 4, "Exit")

	#draw button and check if clicked
	if kinematics.draw(screen):
		gameState = "kinematics"

	if aboutMe.draw(screen):
		gameState = "aboutMe"

	if exit.draw(screen):
		GAME_OVER = True


def draw_kinematics():
	screen.fill(backgroundColor)
	draw_d4()
	pygame.draw.rect(screen, objectsColor, (0, Kinematics.groundHeight, SCREEN_WIDTH, 10))

	#buttons
	return_to_menu_button()

	if kinematicsMass.get_ifAnimating():
		kinematicsAngleBar.draw_static(screen)
		kinematicsHeightBar.draw_static(screen)
		kinematicsVelocityBar.draw_static(screen)

		kinematicsMass.next_launch_frame(5)
		if resetButton.draw(screen):
			kinematicsMass.set_ifAnimating(False)
			kinematicsMass.set_pos(kinematicsMass.originalCenterX, kinematicsMass.originalCenterY)

	elif kinematicsMass.get_ifDoneAnimating():
		kinematicsAngleBar.draw_static(screen)
		kinematicsHeightBar.draw_static(screen)
		kinematicsVelocityBar.draw_static(screen)

		kinematicsMass.after_animation(screen)

		if resetButton.draw(screen):
			kinematicsMass.set_ifAnimating(False)
			kinematicsMass.set_pos(kinematicsMass.originalCenterX, kinematicsMass.originalCenterY)

	else:
		if defaultButton.draw(screen):
			kinematicsAngleBar.set_value(0)
			kinematicsHeightBar.set_value(250)
			kinematicsVelocityBar.set_value(50)

		if launchButton.draw(screen):
			kinematicsMass.set_ifAnimating(True)

		kinematicsAngleBar.draw(screen)
		kinematicsHeightBar.draw(screen)
		kinematicsVelocityBar.draw(screen)

		kinematicsMass.set_angle(kinematicsAngleBar.get_value())
		kinematicsMass.set_pos(kinematicsMass.originalCenterX, Kinematics.groundHeight - Kinematics.massRadius - kinematicsHeightBar.get_value())
		kinematicsMass.set_initial_velocity(kinematicsVelocityBar.get_value())

	kinematicsMass.draw_static(screen)


def draw_about_me():
	screen.fill(backgroundColor)
	draw_d4()
	return_to_menu_button()

	screen.blit(scaledRoj, (SCREEN_WIDTH / 2 - rojWidth / 2, 50))
	draw_text_center(SCREEN_WIDTH / 2, rojWidth + 70, 20, "By Rohil Agarwal")
	draw_text_center(SCREEN_WIDTH / 2, rojWidth + 100, 20, "I go by roj.")
	draw_text_center(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50, 20, "Github: https://github.com/rohilvagarwal")


#game start
draw_menu()
pygame.display.update()

while not GAME_OVER:
	startTime = time.time()

	if gameState == "menu":
		draw_menu()
	if gameState == "kinematics":
		draw_kinematics()
	if gameState == "aboutMe":
		draw_about_me()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			GAME_OVER = True

	pygame.display.update()
	clock.tick(FPS)

	endTime = time.time()
#print(round(1 / (endTime - startTime), 3))

pygame.quit()
sys.exit()
