import random
import pygame
import sys

from pygame.locals import *

speed = 5
body = pygame.image.load('主体.jpg')
body = pygame.transform.scale(body, (30, 30))
bone = pygame.image.load('骨头.png')
bone = pygame.transform.scale(bone, (30, 30))
index = pygame.image.load('图标.png')
index = pygame.transform.scale(index, (900, 600))
icon = pygame.image.load('头像.jpg')
white = (255, 255, 255)
yellow = (238, 173, 14)
brown = (139,175,10)
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4


def main():
	pygame.init()
	clock = pygame.time.Clock()
	screen = pygame.display.set_mode((900, 600))
	screen.fill(white)

	pygame.display.set_caption("贪吃DOG")
	pygame.display.set_icon(icon)
	start(screen)
	while True:
		running_game(screen, clock)
		gameover(screen)


def running_game(screen,clock):
	pygame.mixer_music.load('black space.mp3')
	pygame.mixer_music.play(0, 10)
	startx = random.randint(3, 25)
	starty = random.randint(3, 15)
	dogs = [{'x': startx, 'y': starty}, {'x': startx - 1, 'y': starty}, {'x': startx - 2, 'y': starty}]
	direction = RIGHT
	food = get_random_location()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
					direction = LEFT
				elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
					direction = RIGHT
				elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
					direction = UP
				elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
					direction = DOWN
				elif event.key == K_ESCAPE:
					terminate()
		move(direction, dogs)
		judge = isAlive(dogs)
		if not judge:
			break
		isEat(dogs, food)
		screen.fill(white)
		drawDog(screen, dogs)
		drawFood(screen, food)
		drawScore(screen, len(dogs) - 3)
		pygame.display.update()
		if len(dogs) < 50:
			speed = 6 + len(dogs)//5
		else:
			speed = 16
		clock.tick(speed)


def drawFood(screen, food):
	x = food['x'] * 30
	y = food['y'] * 30
	Rect1 = pygame.Rect(x, y, 30, 30)
	screen.blit(bone, Rect1)


def drawDog(screen, dogs):
	for dog in dogs:
		x = dog['x'] * 30
		y = dog['y'] * 30
		Rect2 = pygame.Rect(x, y, 30, 30)
		screen.blit(body, Rect2)


def move(direction, dogs):
	if direction == UP:
		newHead = {'x': dogs[0]['x'], 'y': dogs[0]['y'] - 1}
	elif direction == DOWN:
		newHead = {'x': dogs[0]['x'], 'y': dogs[0]['y'] + 1}
	elif direction == LEFT:
		newHead = {'x': dogs[0]['x'] - 1, 'y': dogs[0]['y']}
	elif direction == RIGHT:
		newHead = {'x': dogs[0]['x'] + 1, 'y': dogs[0]['y']}
	dogs.insert(0, newHead)


def isAlive(dogs):
	tag = True
	if dogs[0]['x'] == -1 or dogs[0]['x'] == 30 or dogs[0]['y'] == -1 or dogs[0]['y'] == 20:
		tag = False
	for body in dogs[1:]:
		if body['x'] == dogs[0]['x'] and body['y'] == dogs[0]['y']:
			tag = False
	return tag


def isEat(dogs, food):
	if dogs[0]['x'] == food['x'] and dogs[0]['y'] == food['y']:
		food['x'] = random.randint(0, 29)
		food['y'] = random.randint(0, 19)
	else:
		del dogs[-1]


def get_random_location():
	return {'x': random.randint(0, 29), 'y': random.randint(0, 19)}


def start(screen):
	font = pygame.font.Font('fz.ttf', 40)
	tip = font.render('按任意键开始游戏', True, brown)
	screen.blit(index,(0,0))
	screen.blit(tip, (50, 240))
	pygame.mixer_music.load('pikachu.mp3')
	pygame.mixer_music.play(0, 10)
	pygame.display.update()

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if (event.key == K_ESCAPE):
					terminate()
				else:
					return


def gameover(screen):
	font = pygame.font.Font('fz.ttf', 40)
	tip = font.render('按Q或者ESC退出游戏, 按任意键重新开始游戏', True, brown)
	gameover = pygame.image.load('gameover.jpg')
	gameover = pygame.transform.scale(gameover, (900, 600))
	screen.blit(gameover, (0, 0))
	screen.blit(tip, (50, 280))
	pygame.mixer_music.load('Town.mp3')
	pygame.mixer_music.play(0, 10)
	pygame.display.update()

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE or event.key == K_q:
					terminate()
				else:
					return


def drawScore(screen,score):
	font = pygame.font.Font('fz.ttf', 30)
	scoreSurf = font.render('得分: %s' % score, True, yellow)
	scoreRect = scoreSurf.get_rect()
	scoreRect.topleft = (900 - 120, 10)
	screen.blit(scoreSurf, scoreRect)


def terminate():
	pygame.quit()
	sys.exit()


main()
