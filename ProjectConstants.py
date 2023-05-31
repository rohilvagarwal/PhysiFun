import pygame

pygame.init()

#Project Constants
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

#Project Methods
#clicking mechanism
ifMouseDownEarlier = False


def ifClicked():
	global ifMouseDownEarlier

	if pygame.mouse.get_pressed()[0] == 1:
		if not ifMouseDownEarlier:
			ifMouseDownEarlier = True
			#print("Yes")
			return True
	else:
		ifMouseDownEarlier = False

	return False


def rotate_surface(surface, angle, x, y):
	#rotate surface around pivot point
	rotated_surface = pygame.transform.rotate(surface, angle)

	#make pivot point center
	pivotX = x
	pivotY = y
	rect = rotated_surface.get_rect()
	rect.center = pivotX, pivotY

	return rotated_surface, rect


#10, 20, 25, 30, 70
font10 = pygame.font.SysFont("jost700", 10)
font20 = pygame.font.SysFont("jost700", 20)
font25 = pygame.font.SysFont("jost700", 25)
font30 = pygame.font.SysFont("jost700", 30)
font70 = pygame.font.SysFont("jost700", 70)


def draw_text_center(screen, centerX, centerY, textSize, text):
	if textSize == 10:
		font = font10
	elif textSize == 20:
		font = font20
	elif textSize == 25:
		font = font25
	elif textSize == 30:
		font = font30
	elif textSize == 70:
		font = font70
	else:
		font = pygame.font.SysFont("jost700", textSize)

	text = font.render(text, True, textColor)
	text_rect = text.get_rect(center=(centerX, centerY))
	screen.blit(text, text_rect)


def draw_text_left(screen, leftX, centerY, textSize, text):
	if textSize == 10:
		font = font10
	elif textSize == 20:
		font = font20
	elif textSize == 25:
		font = font25
	elif textSize == 30:
		font = font30
	elif textSize == 70:
		font = font70
	else:
		font = pygame.font.SysFont("jost700", textSize)

	text = font.render(text, True, textColor)
	text_rect = text.get_rect(left=leftX, centery=centerY)
	screen.blit(text, text_rect)


def draw_text_right(screen, rightX, centerY, textSize, text):
	if textSize == 10:
		font = font10
	elif textSize == 20:
		font = font20
	elif textSize == 25:
		font = font25
	elif textSize == 30:
		font = font30
	elif textSize == 70:
		font = font70
	else:
		font = pygame.font.SysFont("jost700", textSize)

	text = font.render(text, True, textColor)
	text_rect = text.get_rect(right=rightX, centery=centerY)
	screen.blit(text, text_rect)


def draw_text_top_left(screen, leftX, topY, textSize, text):
	if textSize == 10:
		font = font10
	elif textSize == 20:
		font = font20
	elif textSize == 25:
		font = font25
	elif textSize == 30:
		font = font30
	elif textSize == 70:
		font = font70
	else:
		font = pygame.font.SysFont("jost700", textSize)

	text = font.render(text, True, textColor)
	screen.blit(text, (leftX, topY))
