from ProjectConstants import *

rojWidth = 300
roj = pygame.image.load('images/roj.png').convert_alpha()
scaledRoj = pygame.transform.scale(roj, (rojWidth, rojWidth)).convert_alpha()


def draw_about_me(screen):
	screen.blit(scaledRoj, (SCREEN_WIDTH / 2 - rojWidth / 2, 50))
	draw_text_center(screen, SCREEN_WIDTH / 2, rojWidth + 70, 20, "By Rohil Agarwal")
	draw_text_center(screen, SCREEN_WIDTH / 2, rojWidth + 100, 20, "I go by roj.")
	draw_text_center(screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50, 20, "Github: https://github.com/rohilvagarwal")
