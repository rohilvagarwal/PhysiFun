import asyncio
import pygame

from ProjectConstants import *

import sys
from ExtraPages.Menu import draw_menu
from ExtraPages.LearnMore import draw_about_me
from UIElements.Button import Button
from PhysicsModules.Kinematics import Kinematics
from PhysicsModules.CircularMotion import CircularMotion
import time


def update_game_state(new_state):
	global gameState
	gameState = new_state


def all_pages():
	screen.fill(backgroundColor)

	global gameState

	#return to menu button
	if gameState != "menu":
		menuButton = Button(centerX=SCREEN_WIDTH - 75, centerY=50, width=100, height=50, textSize=30, borderSize=10, text="Menu")

		if menuButton.draw_and_check_click(screen):
			gameState = "menu"


#game states: menu, kinematics, circularMotion, aboutMe
gameState = "menu"

#objects
kinematicsObj = Kinematics(100, 500, 50, 0)
circularMotionObj = CircularMotion(SCREEN_WIDTH / 2 - 250, CircularMotion.groundHeight / 2, 10)


async def main():
	#game start
	#game variables
	GAME_OVER = False

	all_pages()
	draw_menu(screen, update_game_state)
	pygame.display.update()

	frame_count = 0
	frame_rate = 0
	start_time = time.time()

	while not GAME_OVER:
		#startTime = time.time()
		all_pages()

		if gameState == "menu":
			draw_menu(screen, update_game_state)
		if gameState == "kinematics":
			kinematicsObj.draw_static(screen)
		if gameState == "circularMotion":
			circularMotionObj.draw_static(screen, 0.1)  #1 pixel is 0.1m
		if gameState == "aboutMe":
			draw_about_me(screen)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				GAME_OVER = True

		frame_count += 1
		if time.time() - start_time > 1:
			frame_rate = frame_count
			frame_count = 0
			start_time = time.time()

		draw_text_left(screen, 5, 10, 10, "FPS: " + str(frame_rate))

		pygame.display.update()
		clock.tick(FPS)
		await asyncio.sleep(0)

	#endTime = time.time()
	#print(round(1 / (endTime - startTime), 3))

	pygame.quit()
	sys.exit()


asyncio.run(main())
