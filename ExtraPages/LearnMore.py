from ProjectConstants import *

rojWidth = 300
roj = pygame.image.load('images/roj.png').convert_alpha()
scaledRoj = pygame.transform.scale(roj, (rojWidth, rojWidth)).convert_alpha()


def draw_about_me(screen):
	screen.blit(scaledRoj, (SCREEN_WIDTH / 2 - rojWidth / 2, 50))
	draw_text_center(screen, SCREEN_WIDTH / 2, rojWidth + 70, 20, "By Rohil Agarwal")
	draw_text_center(screen, SCREEN_WIDTH / 2, rojWidth + 100, 20,
					 "This Physics Visualization App is an innovative tool designed to enhance your understanding")
	draw_text_center(screen, SCREEN_WIDTH / 2, rojWidth + 100 + 20, 20,
					 "and visualization of concepts in Physics I. The app provides real-time simulations that allow")
	draw_text_center(screen, SCREEN_WIDTH / 2, rojWidth + 100 + 40, 20,
					 "you to interact with physics concepts and observe their behavior as if you were conducting")
	draw_text_center(screen, SCREEN_WIDTH / 2, rojWidth + 100 + 60, 20,
					 " real experiments. Whether you're a student, educator, or just someone curious about physics,")
	draw_text_center(screen, SCREEN_WIDTH / 2, rojWidth + 100 + 80, 20,
					 "this app is your gateway to learn more in an interesting way!")
	draw_text_center(screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50, 20, "Github: https://github.com/rohilvagarwal")
	draw_text_center(screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 25, 20, "LinkedIn: https://www.linkedin.com/in/rohil-ag/")
