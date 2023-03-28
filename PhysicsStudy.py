import pygame
import sys
from ProjectConstants import *
from Button import *

pygame.init()

#game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

#game variables
GAME_OVER = False
clock = pygame.time.Clock()
FPS = 60
gameState = "menu"


def draw_text_center(centerX, centerY, textSize, text):
	font = pygame.font.SysFont("jost700", textSize)
	text = font.render(text, True, textColor)
	text_rect = text.get_rect(center=(centerX, centerY))
	screen.blit(text, text_rect)


def draw_menu():
	screen.fill(backgroundColor)

	#draw title
	draw_text_center(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 10, 70, "PhysicsStudy")
	draw_text_center(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 5, 30, "By Rohil Agarwal")

	hello = Button(centerX=200, centerY=200, width=200, height=200, textSize=50, borderSize=10, text="empty")
	if hello.draw(screen):
		print("clicked")


#game start
draw_menu()

pygame.display.update()

while not GAME_OVER:
	if gameState == "menu":
		draw_menu()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			GAME_OVER = True

	pygame.display.update()
	clock.tick(FPS)

pygame.quit()
sys.exit()
