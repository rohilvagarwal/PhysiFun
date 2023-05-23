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

#game states: menu, kinematics, circularMotion, aboutMe
gameState = "menu"

#kinematics
kinematicsAngleBar = SliderBar(25, SCREEN_HEIGHT - 50, 200, 20, -90, 90, 0, "Angle (°)")
kinematicsHeightBar = SliderBar(250, SCREEN_HEIGHT - 50, 200, 20, 0, 500, 250, "Height (m)")
kinematicsVelocityBar = SliderBar(475, SCREEN_HEIGHT - 50, 200, 20, 0, 100, 50, "Initial Velocity (m/s)")
kinematicsMass = Kinematics(100, 500, 100, 0)
launchButton = Button(centerX=SCREEN_WIDTH - 125, centerY=SCREEN_HEIGHT - 40, width=200, height=50, textSize=30, borderSize=10, text="Launch")
defaultButton = Button(centerX=SCREEN_WIDTH - 125, centerY=SCREEN_HEIGHT - 95, width=200, height=50, textSize=30, borderSize=10, text="Default")
pauseButton = Button(centerX=SCREEN_WIDTH - 125, centerY=SCREEN_HEIGHT - 40, width=200, height=50, textSize=30, borderSize=10, text="Pause")
resetButton = Button(centerX=SCREEN_WIDTH - 125, centerY=SCREEN_HEIGHT - 95, width=200, height=50, textSize=30, borderSize=10, text="Reset")


def draw_text_center(centerX, centerY, textSize, text):
	font = pygame.font.SysFont("jost700", textSize)
	text = font.render(text, True, textColor)
	text_rect = text.get_rect(center=(centerX, centerY))
	screen.blit(text, text_rect)


def menu_button(centerY, text):
	return Button(centerX=200, centerY=centerY, width=230, height=50, textSize=30, borderSize=10, text=text)


def return_to_menu_button():
	global gameState

	menuButton = Button(centerX=SCREEN_WIDTH - 75, centerY=50, width=100, height=50, textSize=30, borderSize=10, text="Menu")

	if menuButton.draw_and_check_click(screen):
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

	kinematics = menu_button(2 * SCREEN_HEIGHT / 6, "Kinematics")
	circularMotion = menu_button(3 * SCREEN_HEIGHT / 6, "Circular Motion")
	aboutMe = menu_button(4 * SCREEN_HEIGHT / 6, "About Me")
	exit = menu_button(5 * SCREEN_HEIGHT / 6, "Exit")

	#draw button and check if clicked
	if kinematics.draw_and_check_click(screen):
		gameState = "kinematics"

	if circularMotion.draw_and_check_click(screen):
		gameState = "circularMotion"

	if aboutMe.draw_and_check_click(screen):
		gameState = "aboutMe"

	if exit.draw_and_check_click(screen):
		GAME_OVER = True


def draw_kinematics():
	screen.fill(backgroundColor)
	draw_d4()
	pygame.draw.rect(screen, objectsColor, (0, Kinematics.groundHeight, SCREEN_WIDTH, 10))

	#buttons
	return_to_menu_button()

	if kinematicsMass.get_state() == "animating":
		kinematicsAngleBar.draw_static(screen)
		kinematicsHeightBar.draw_static(screen)
		kinematicsVelocityBar.draw_static(screen)

		if pauseButton.draw_and_check_click(screen):
			kinematicsMass.set_state("paused")

		if resetButton.draw_and_check_click(screen):
			kinematicsMass.set_state("default")
			kinematicsMass.set_pos(kinematicsMass.originalCenterX, kinematicsMass.originalCenterY)

		kinematicsMass.next_launch_frame(5)

	elif kinematicsMass.get_state() == "paused":
		kinematicsAngleBar.draw_static(screen)
		kinematicsHeightBar.draw_static(screen)
		kinematicsVelocityBar.draw_static(screen)

		if pauseButton.draw_and_check_click(screen):
			kinematicsMass.set_state("animating")

		if resetButton.draw_and_check_click(screen):
			kinematicsMass.set_state("default")
			kinematicsMass.set_pos(kinematicsMass.originalCenterX, kinematicsMass.originalCenterY)

	elif kinematicsMass.get_state() == "doneAnimating":
		kinematicsAngleBar.draw_static(screen)
		kinematicsHeightBar.draw_static(screen)
		kinematicsVelocityBar.draw_static(screen)

		kinematicsMass.after_animation(screen)

		if resetButton.draw_and_check_click(screen):
			kinematicsMass.set_state("default")
			kinematicsMass.set_pos(kinematicsMass.originalCenterX, kinematicsMass.originalCenterY)

	elif kinematicsMass.get_state() == "default":
		if defaultButton.draw_and_check_click(screen):
			kinematicsAngleBar.set_value(0)
			kinematicsHeightBar.set_value(250)
			kinematicsVelocityBar.set_value(50)

		kinematicsAngleBar.draw(screen)
		kinematicsHeightBar.draw(screen)
		kinematicsVelocityBar.draw(screen)

		kinematicsMass.set_angle(kinematicsAngleBar.get_value())
		kinematicsMass.set_pos(kinematicsMass.originalCenterX, Kinematics.groundHeight - Kinematics.massRadius - kinematicsHeightBar.get_value())
		kinematicsMass.set_initial_velocity(kinematicsVelocityBar.get_value())

		if launchButton.draw_and_check_click(screen):
			kinematicsMass.set_state("animating")

	kinematicsMass.draw_static(screen)


def draw_circular_motion():
	screen.fill(backgroundColor)
	draw_d4()
	return_to_menu_button()


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
	if gameState == "circularMotion":
		draw_circular_motion()
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
