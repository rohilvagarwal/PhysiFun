from ProjectConstants import *
from UIElements.Button import Button


def menu_button(centerX, centerY, text):
	return Button(centerX=centerX, centerY=centerY, width=230, height=50, textSize=30, borderSize=10, text=text)


def draw_menu(screen, update_game_state):
	#draw title
	logo_rect = scaled_logo.get_rect(center=(SCREEN_WIDTH / 2, 150))
	screen.blit(scaled_logo, logo_rect)  #draw d4
	draw_text_center(screen, SCREEN_WIDTH / 3, SCREEN_HEIGHT / 4 + 10, 30, "By Rohil Agarwal")

	kinematics = menu_button(200, 3 * SCREEN_HEIGHT / 6, "Kinematics")
	circularMotion = menu_button(200, 4 * SCREEN_HEIGHT / 6, "Circular Motion")
	learnMore = menu_button(200, 5 * SCREEN_HEIGHT / 6, "Learn More")

	#draw button and check if clicked
	if kinematics.draw_and_check_click(screen):
		update_game_state("kinematics")

	if circularMotion.draw_and_check_click(screen):
		update_game_state("circularMotion")

	if learnMore.draw_and_check_click(screen):
		update_game_state("learnMore")
