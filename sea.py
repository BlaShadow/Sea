#!/usr/bin/env python

from threading import Thread
from threading import Lock
import pygame 
import random
import math

from config import fish_options
from fish import *

class Sea():
	""" Screen game """

	def __init__(self):
		""" init method """

		#init game
		pygame.init()

		self.fishs = []

		#setup size
		self.width = 700
		self.height = 300

		#setup screen
		self.screen = pygame.display.set_mode((self.width,self.height),0,16)

		self.bg_color = (51,153,255)
		self.deads = []

		self.paredes = [
			pygame.Rect(0,0,10,self.height),
			pygame.Rect(0,0,self.width,30),
			pygame.Rect(self.width,0,10,self.height),
			pygame.Rect(0,self.height,self.width,10)
		]

		self.xLines = [pygame.Rect(i,0,1,self.height) for i in range(0,self.width,fish_options['fish_space'])]

		self.yLines = [pygame.Rect(0,i,self.width,2) for i in range(0,self.height,fish_options['fish_space'])]

		self.water = [[None for i in range(self.height / fish_options['fish_space'] + 1 )] for i in range(self.width / fish_options['fish_space'] + 1 )]

		self.reloj = pygame.time.Clock()

		self.make_stage()

	def make_stage(self):
		""" Build stage """
		
		self.populate_sea('m', Shark, 7, FishMove.get_move())
		self.populate_sea('w', Shark, 4, FishMove.get_move())
		self.populate_sea('w', Fish, 10, FishMove.get_move())
		self.populate_sea('m', Fish, 15, FishMove.get_move())

		start = False
		done = False

		while done == False:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					done = True
					for item_fish in self.fishs:
						item_fish.dead()

			self.reloj.tick(10)	

			self.screen.fill(self.bg_color)

			# for pared in self.paredes:
			# 	pygame.draw.rect(self.screen,[0,0,200],pared)

			for line in self.xLines:
				pygame.draw.rect(self.screen, [123, 56, 200], line)				

			for line in self.yLines:
				pygame.draw.rect(self.screen, [180, 12, 200], line)								

			writeFile(self.water)

			if start == False:
				for item_fish in self.fishs:
					item_fish.start()
				start = True

			for item_fish in self.fishs:
				if item_fish.alive == True:
					self.screen.blit(item_fish.draw.image, item_fish.draw.rect.move(item_fish.x,i tem_fish.y))

			pygame.display.update()

		exit()

	def populate_sea(self,sexo,fish_type,quantity,move):
		""" fill the sea with items """

		for i in range(quantity):
			fish = fish_type(sexo, fish_type.__name__.lower(), self,move)
			
			self.fishs.append(fish)

def writeFile(items):
	l = Lock()
	l.acquire(True)

	screen = open('screen','w')
	screen.write("\n\n\n")
	screen.write("\n==============\n")

	for item in items:
		line = ""
		for x,i in enumerate(item):
			if i == None:
				line = line + "[]"
			else:
				if i.__class__ == Shark:
					line = line + "[X]"
		screen.write(line + "\n")

	screen.write("\n==============\n")
	screen.close()

	l.release()
