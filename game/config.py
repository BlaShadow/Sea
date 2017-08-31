#config
import pygame 

fish_options = {
	'fish_space':32,
	'dead':pygame.image.load("dead.png"),
	'baby':pygame.image.load("baby.png"),
	'fish':{
		'm':{
			'pic' : pygame.image.load("imgs/fish.png"),
			'speed' : 2,
		},

		'w':{
			'pic' : pygame.image.load("imgs/fish_w.png"),
			'speed' : 2,
		}
	},
	'shark':{
		'm':{
			'pic' : pygame.image.load("imgs/shark.png"),
			'speed' : 10,
		},

		'w':{
			'pic' : pygame.image.load("imgs/shark_w.png"),
			'speed' : 10,
		}
	}
}
