import pygame
import sys
from ProjectConstants import *
from Button import *
from SliderBar import *
from MassMath import *
import time

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

#game variables
GAME_OVER = False

#game states: menu, kinematics, about me
gameState = "kinematics"

#make sliders
kinematicsSliderBar = SliderBar(SCREEN_WIDTH - 425, SCREEN_HEIGHT - 150, 400, 20, -90, 90, 0)

#make masses
kinematicsMass = MassMath(100, 500, 100, 0)

#make buttons
launchButton = Button(centerX=SCREEN_WIDTH - 125, centerY=SCREEN_HEIGHT - 50, width=200, height=50, textSize=30, borderSize=10, text="Launch")
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


def draw_menu():
	global gameState
	global GAME_OVER
	screen.fill(backgroundColor)

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

	#buttons
	return_to_menu_button()

	kinematicsSliderBar.draw(screen)

	# #if not animating and not done animating
	# if kinematicsMass.get_ifAnimating() is False and kinematicsMass.get_ifDoneAnimating() is False:
	# 	#check if launch button is pressed
	# 	if launchButton.draw(screen):
	# 		kinematicsMass.set_ifAnimating(True)
	# else:
	# 	if resetButton.draw(screen):
	# 		kinematicsMass.set_ifAnimating(False)
	# 		kinematicsMass.set_pos(kinematicsMass.originalCenterX, kinematicsMass.originalCenterY)

	if kinematicsMass.get_ifAnimating():
		kinematicsMass.next_launch_frame(5)
		if resetButton.draw(screen):
			kinematicsMass.set_ifAnimating(False)
			kinematicsMass.set_pos(kinematicsMass.originalCenterX, kinematicsMass.originalCenterY)
	elif kinematicsMass.get_ifDoneAnimating():
		if resetButton.draw(screen):
			kinematicsMass.set_ifAnimating(False)
			kinematicsMass.set_pos(kinematicsMass.originalCenterX, kinematicsMass.originalCenterY)
	else:
		kinematicsMass.set_angle(kinematicsSliderBar.get_value())
		if launchButton.draw(screen):
			kinematicsMass.set_ifAnimating(True)

	kinematicsMass.draw_static(screen)


def draw_about_me():
	screen.fill(backgroundColor)
	return_to_menu_button()


#game start
draw_menu()
pygame.display.update()

while not GAME_OVER:
	startTime = time.time()

	ifClicked()

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
