import pygame
import math

pygame.init()

#Project Constants
#game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = SCREEN_WIDTH * 0.7

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

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

#Game Logo
logo = pygame.image.load('images/PhysiFun Logo 800x600.svg').convert_alpha()
scaled_logo = pygame.transform.scale(logo, (600, 450)).convert_alpha()

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
font10 = pygame.font.Font("fonts/Jost-700-Bold.otf", 10)
font20 = pygame.font.Font("fonts/Jost-700-Bold.otf", 20)
font25 = pygame.font.Font("fonts/Jost-700-Bold.otf", 25)
font30 = pygame.font.Font("fonts/Jost-700-Bold.otf", 30)
font70 = pygame.font.Font("fonts/Jost-700-Bold.otf", 70)


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
		font = pygame.font.Font("fonts/Jost-700-Bold.otf", textSize)

	text = font.render(text, True, textColor)
	text_rect = text.get_rect(center=(centerX, centerY))
	screen.blit(text, text_rect)

	return (textSize, text_rect.right, centerY)


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
		font = pygame.font.Font("fonts/Jost-700-Bold.otf", textSize)

	text = font.render(text, True, textColor)
	text_rect = text.get_rect(left=leftX, centery=centerY)
	screen.blit(text, text_rect)

	return (textSize, text_rect.right, centerY)


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
		font = pygame.font.Font("fonts/Jost-700-Bold.otf", textSize)

	text = font.render(text, True, textColor)
	text_rect = text.get_rect(right=rightX, centery=centerY)
	screen.blit(text, text_rect)

	return (textSize, text_rect.right, centerY)


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
		font = pygame.font.Font("fonts/Jost-700-Bold.otf", textSize)

	text = font.render(text, True, textColor)
	screen.blit(text, (leftX, topY))


def draw_superscript(screen, positionTuple, text):
	text = font10.render(text, True, textColor)
	text_rect = text.get_rect(left=positionTuple[1], top=positionTuple[2] - positionTuple[0] * 3 / 5)
	screen.blit(text, text_rect)

	return text_rect.right


def draw_left_with_superscript(screen, leftX, centerY, textSize, text):
	split_text = text.split('^')
	cleaned_text = [sub_text for sub_text in split_text if sub_text]

	lastRightCoordinate = leftX

	for n in range(len(cleaned_text)):
		if n % 2 == 0:
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
				font = pygame.font.Font("fonts/Jost-700-Bold.otf", textSize)

			text = font.render(cleaned_text[n], True, textColor)
			text_rect = text.get_rect(left=lastRightCoordinate, centery=centerY)
			screen.blit(text, text_rect)

			lastRightCoordinate = text_rect.right

		if n % 2 == 1:
			text = font10.render(cleaned_text[n], True, textColor)
			text_rect = text.get_rect(left=lastRightCoordinate, top=centerY - textSize * 3 / 5)
			screen.blit(text, text_rect)

			lastRightCoordinate = text_rect.right


def draw_left_with_subscript(screen, leftX, centerY, textSize, text):
	split_text = text.split('_')
	cleaned_text = [sub_text for sub_text in split_text if sub_text]

	lastRightCoordinate = leftX

	for n in range(len(cleaned_text)):
		if n % 2 == 0:
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
				font = pygame.font.Font("fonts/Jost-700-Bold.otf", textSize)

			text = font.render(cleaned_text[n], True, textColor)
			text_rect = text.get_rect(left=lastRightCoordinate, centery=centerY)
			screen.blit(text, text_rect)

			lastRightCoordinate = text_rect.right

		if n % 2 == 1:
			text = font10.render(cleaned_text[n], True, textColor)
			text_rect = text.get_rect(left=lastRightCoordinate, top=centerY + textSize * 1 / 10)
			screen.blit(text, text_rect)

			lastRightCoordinate = text_rect.right


def degrees_to_mouse(centerX, centerY):
	# Get the mouse position
	mouse_x, mouse_y = pygame.mouse.get_pos()

	# Calculate the angle between the arrow and the mouse position
	dx = mouse_x - centerX
	dy = mouse_y - centerY
	return math.degrees(math.atan2(-dy, dx))

def blit_center(screen, image, coordinates):
	image_rect = image.get_rect()

	blit_x = coordinates[0] - (image_rect.width // 2)
	blit_y = coordinates[1] - (image_rect.height // 2)

	screen.blit(image, (blit_x, blit_y))