import pygame
import sys
from ProjectConstants import *
from Button import *
from SliderBar import *
import time

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

#game variables
GAME_OVER = False

#game states: menu, kinematics, about me
gameState = "kinematics"


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
	global kinematicsSliderBar
	screen.fill(backgroundColor)
	return_to_menu_button()

	kinematicsSliderBar.draw(screen)


def draw_about_me():
	screen.fill(backgroundColor)
	return_to_menu_button()


#game start
draw_menu()
pygame.display.update()

#make sliders
kinematicsSliderBar = SliderBar(SCREEN_WIDTH - 475, SCREEN_HEIGHT - 75, 400, 20, 0, 100, 50)

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
