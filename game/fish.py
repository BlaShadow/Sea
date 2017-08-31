#!/usr/bin/env python

from threading import Thread
from threading import Lock
from config import fish_options

import thread
import random
import pygame 
import math

class FishDesc():
	def __init__(self, initval=None, name='var'):
		if initval == None:
			raise Exception('Invalid value')

		if not isinstance(initval, Fish):
			raise Exception('Invalid value need a {} and pased a {}'.format(type(Fish), type(initval)))

		self.val = initval

	def __get__(self):
		return self.val

	def __set__(self, obj, val):
		self.val = val


class FishDrawDesc():
	def __init__(self, initval=pygame.sprite.Sprite(), name='var'):
		self.obj = initval
		self.name = name

	def __get__(self):
		return self.obj

	def __set__(self,obj,val):
		if isinstance(pygame.sprite.Sprite, val):
			raise Exception('Not correct instace')

		self.obj = val

class Fish(Thread):
	x = 0
	y = 0

	def __init__(self, sexo, fish_type, sea,move):
		Thread.__init__(self)

		self.fish_type = fish_type
		self.sex = sexo
		
		obj = FishDraw(fish_options[fish_type][sexo]['pic'])

		self.draw = obj.draw
		self.sea = sea
		self.screen = sea.screen
		self.speed = fish_options[fish_type][sexo]['speed']

		self.reloj = pygame.time.Clock()

		self.move = move

		self.lock = Lock()

		self.alive = True

	def log(self, x, y):
		pass
		# file = open(self.name,'w')
		
		# data = "x: {} y: {} \n".format(x,y)
		
		# file.write(data)
		# file.close()

	def run(self):
		self.x = random.randint(0, self.sea.width)
		self.y = random.randint(0, self.sea.height)

		x = self.x / fish_options['fish_space']
		y = self.y / fish_options['fish_space']

		self.move(self)

		while self.alive:

			self.reloj.tick(1 + self.speed )

			prevX = self.x
			prevY = self.y	

			if self.x > self.sea.width or self.x < 0:
				self.x = 0

			if self.y > self.sea.height or self.y < 0:
				self.y = 0

			if prevY != self.y or prevX != self.x:
				FishMove.move_on_water(prevX, prevY, self.sea, None)

			self.move(self)
		self.sea.fishs.remove(self)

	def dead(self):
		self.alive = False
		self.move(self, dead=True)
		self.sea.fishs.remove(self)


	def fight(self,fish):
		if self != fish:
			
			if self.__class__.__name__ == fish.__class__.__name__:
				if random.randint(1, 4) > 2:
					self.dead()
				else:
					fish.dead()
			else:
				self.dead()
		else:
			print "him self"

	def make_baby(self):
		sexo = 'w' if random.randint(0,10) > 5 else 'm'

		fish = self.__class__(sexo, self.__class__.__name__.lower(), self.sea, FishMove.fish_move)
		fish.start()

		self.sea.fishs.append(fish)

class Shark(Fish):
	def __init__(self, sexo, fish_type, sea,move):

		Fish.__init__(self, sexo, fish_type, sea, move)

	def fight(self, fish):
		if self != fish:
			try:
				if self.__class__.__name__ == fish.__class__.__name__:
					if random.randint(1, 10) > 5:
						self.dead()
					else:
						fish.dead()
				else:
					fish.dead()
			except Exception, e:
				print 'exceptrion como asi ',e.message
		else: 
			print "Him self"

class FishMove():

	@classmethod
	def get_move(self):
		moves = [FishMove.shark_move, FishMove.random, FishMove.fish_move]

		return moves[random.randint(0,2)]

	@classmethod
	def move_on_water(self, x, y, sea,obj):
		tmpx = x
		tmpy = y
		y = y / fish_options['fish_space']
		x = x / fish_options['fish_space']

		try:
			if obj == None:
				sea.water[x][y] = None
				return			

			obj.log(x,y)

			if sea.water[x][y] == None:
				sea.water[x][y] = obj
			else:
				if obj != None and sea.water[x][y] != obj:
					if obj.sex == sea.water[x][y].sex and sea.water[x][y].__class__ == obj.__class__:
						obj.fight(sea.water[x][y])
						return

					if obj.sex != sea.water[x][y].sex and sea.water[x][y].__class__ == obj.__class__:
						obj.make_baby()
						return

					if sea.water[x][y].__class__ != obj.__class__:
						obj.fight(sea.water[x][y])
						return

		except Exception as e:
			pass

	@classmethod
	def move_sin(self, fish, **kwarg):
		fish.lock.acquire(True)

		self.move_on_water(fish.x, fish.y, fish.sea, None)

		fish.x = fish.x + 4 
		fish.y = fish.y + 2

		self.move_on_water(fish.x, fish.y, fish.sea, fish)

		fish.lock.release()

	@classmethod
	def fish_move(self, fish, **kwarg):
		fish.lock.acquire(True)

		if kwarg != None and 'dead' in kwarg:
			self.move_on_water(fish.x, fish.y, fish.sea, None)
			return			

		self.move_on_water(fish.x, fish.y, fish.sea,None)

		fish.x = fish.x + 1
		fish.y = fish.y + 1

		self.move_on_water(fish.x, fish.y, fish.sea, fish)

		fish.lock.release()

	@classmethod
	def shark_move(self,fish,**kwarg):
		fish.lock.acquire(True)

		if kwarg != None and 'dead' in kwarg:
			self.move_on_water(fish.x, fish.y, fish.sea, None)
			return

		self.move_on_water(fish.x, fish.y, fish.sea, None)
		
		fish.x = fish.x + 1

		self.move_on_water(fish.x, fish.y, fish.sea, fish)

		fish.lock.release()

	@classmethod
	def random(self, fish, **kwarg):
		fish.lock.acquire(True)

		if kwarg != None and 'dead' in kwarg:
			self.move_on_water(fish.x, fish.y, fish.sea, None)
			return

		self.move_on_water(fish.x, fish.y, fish.sea, None)
		
		fish.x,fish.y = self.get_direction(fish.x, fish.y)

		self.move_on_water(fish.x, fish.y, fish.sea, fish)

		fish.lock.release()

	@classmethod
	def get_direction(self, x, y):
		result = random.randint(0, 4)

		if result == 1:
			x = x + 1
		elif result == 2:
			x = x - 1
		elif result == 3:
			y = y + 1
		elif result == 4:
			y = y - 1
		return x,y


class FishDraw():
	def __init__(self,img):
		self.draw = FishDrawDesc()
		self.draw.image = img
		self.draw.rect = self.draw.image.get_rect()
