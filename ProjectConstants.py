import pygame

#clicking mechanism
ifMouseDownEarlier = False


def ifClicked():
	global ifMouseDownEarlier

	if not ifMouseDownEarlier:
		if pygame.mouse.get_pressed()[0] == 1:
			ifMouseDownEarlier = True
			print("Yes")
			return True
	if ifMouseDownEarlier is True:
		if pygame.mouse.get_pressed()[0] == 1:
			return False
		elif pygame.mouse.get_pressed()[0] == 0:
			ifMouseDownEarlier = False
			return False


#game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

#game variables
clock = pygame.time.Clock()
FPS = 60

#colors
WHITE = pygame.Color("#FFFFFF")
BLACK = pygame.Color("#000000")
LIGHT_GREY = pygame.Color("#D3D3D3")
RED = pygame.Color("#FF0000")

backgroundColor = WHITE
textColor = BLACK
hoverColor = LIGHT_GREY
sliderBarColor = BLACK
sliderBarHandleColor = RED
objectsColor = BLACK

#physical constants
GRAVITY = 9.8

#miscellaneous
massRadius = 20
