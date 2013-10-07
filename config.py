#config
import pygame 

fish_options = {
	'fish_space':32,
	
	'dead': pygame.image.load("dead.png"),

	'baby':pygame.image.load("baby.png"),

	'fish':{
		'm':{
			'pic' : pygame.image.load("fish.png"),
			'speed' : 2,
		},

		'w':{
			'pic' : pygame.image.load("fish_w.png"),
			'speed' : 2,
		}		
	},
	'shark':{
		'm':{
			'pic' : pygame.image.load("shark.png"),
			'speed' : 10,
		},

		'w':{
			'pic' : pygame.image.load("shark_w.png"),
			'speed' : 10,
		}
	}
}
