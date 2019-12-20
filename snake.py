#!/usr/bin/env python3

#Importing modules
#--------------------

from random import randint
import pygame as py
py.init()			#Initializing the module

#Classes
#--------------------

class snake:
	def __init__(self):
		self.l = 1					#Length of snake
		self.size = 20				#Size of unit snake
		self.xpos = [0] 			#X_Position of the snake squares
		self.ypos = [0] 			#Y_Position of the snake squares
		self.clr = [0,255,0]		#Colour of snake
		self.xdir = 1				#X_Direction
		self.ydir = 0				#Y_Direction

class board:
	def __init__(self,sn):
		self.brd_size = 20			#Board size(Number of squares along each direction)
		self.fruit_x = sn.size*1
		self.fruit_y = sn.size*1
		self.state = True

#Global state variables

clock = py.time.Clock()	#FPS Counter
s1 = snake()			#Creating the snake
b1 = board(s1)			#Creating the board
win = py.display.set_mode([b1.brd_size*s1.size,b1.brd_size*s1.size])
py.display.set_caption("SNAKE")

#Functions
#---------------------

def draw_snake(sn,blk):
	for i in range(sn.l):
		py.draw.rect(win,sn.clr,(sn.xpos[i],sn.ypos[i],sn.size,sn.size))
	py.draw.rect(win,blk[1],blk[0])

def fruit_gen(sn,b):
	c = randint(0,b.brd_size*b.brd_size - sn.l - 1)
	r = c//b.brd_size
	c = c%b.brd_size
	r = r*sn.size
	c = c*sn.size
	cnt = 0
	for i in range(sn.l):
		if sn.xpos[i] < r:
			cnt+=sn.size
	cnt = cnt + c
	c = 0
	while cnt>0:
		c+=sn.size
		if c==b.brd_size*sn.size:
			r+=sn.size
			c = 0
		for i in range(sn.l):
			if [sn.xpos[i],sn.ypos[i]] == [c,r]:
				cnt+=sn.size
				break
		cnt-=sn.size
	b.fruit_y = r
	b.fruit_x = c
	return [c,r,sn.size,sn.size]

def collision_snake (sn,b):
	if sn.xpos[0] < 0 or sn.xpos[0] == b.brd_size*sn.size:
		b1.state = False
	elif sn.ypos[0] < 0 or sn.ypos[0] == b.brd_size*sn.size:
		b1.state = False
	else:
		for i in range(1,sn.l,1):
			if [sn.xpos[0],sn.ypos[0]] == [sn.xpos[i],sn.ypos[i]]:
				b1.state = False

def update_snake(sn,b):
	#Adding the new position of head based on the inputs
	clr = [0,0,0]			#Default colour to update 
	if sn.xdir == 1:
		sn.xpos.insert(0,sn.xpos[0]+sn.size)
		sn.ypos.insert(0,sn.ypos[0])
	elif sn.xdir == -1:
		sn.xpos.insert(0,sn.xpos[0]-sn.size)
		sn.ypos.insert(0,sn.ypos[0])
	elif sn.ydir ==	1:
		sn.xpos.insert(0,sn.xpos[0])
		sn.ypos.insert(0,sn.ypos[0]-sn.size)
	else:
		sn.xpos.insert(0,sn.xpos[0])
		sn.ypos.insert(0,sn.ypos[0]+sn.size)
	#Check if new position of head coincide with fruit
	if [sn.xpos[0],sn.ypos[0]] == [b.fruit_x,b.fruit_y]:
		sn.l+=1
		extr = fruit_gen(sn,b)		#Returns rectangle of new fruit
		clr = [255,0,0]
	else:
		extr = [sn.xpos.pop(),sn.ypos.pop(),sn.size,sn.size]
		collision_snake(sn,b)			#Collision check for the snake
	return [extr,clr]	

def input_snake(sn):
	key_list = py.key.get_pressed()
	if key_list[py.K_UP]:
		sn.xdir = 0
		sn.ydir = 1
	elif key_list[py.K_DOWN]:
		sn.xdir = 0
		sn.ydir = -1
	elif key_list[py.K_RIGHT]:
		sn.xdir = 1
		sn.ydir = 0
	elif key_list[py.K_LEFT]:
		sn.xdir = -1
		sn.ydir = 0 

#Main pygame loop
#-------------------

py.draw.rect(win,[255,0,0],[b1.fruit_x,b1.fruit_y,s1.size,s1.size])
max_point = b1.brd_size*b1.brd_size

while b1.state:
	clock.tick(6)
	if s1.l == max_point:
		break
	for event in py.event.get():
		if event.type == py.QUIT:	#For quitting the game
			state = False
	input_snake(s1)					#Gets input from the keyboard
	blk = update_snake(s1,b1)	#Generates the rects for the snake
	draw_snake(s1,blk)			#Draws the snake and removes tail
	py.display.update()
py.quit()
print ("Score is : ",s1.l)