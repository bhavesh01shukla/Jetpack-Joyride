from colorama import Fore, Back, Style 
import os
import sys
from collisions import check_collision
import board

class person:
	def __init__(self,xcor,ycor,rows,columns):
		print("a person is created")
		self._xcor=xcor
		self._ycor=ycor
		self._rows=rows	
		self._columns=columns
		self._shape=[]
		self._lives=50
		self._coins=0


	def give_coins(self):
		return self._coins

	def update_coins(self,new_value):
		self._coins=new_value

	def give_lives(self):
		return self._lives
	
	def decrease_lives(self):
		self._lives-=1
		# return self._lives

	def give_xcor(self):
		return self._xcor

	def give_ycor(self):
		return self._ycor

	def give_rows(self):
		return self._rows

	def give_columns(self):
		return self._columns

	def give_shape(self):
		return self._shape

	def movement_possible(self,direction,grid_rows,grid_columns,first_dis_column,last_dis_column,l,vel,grid):
		# print(direction)
		if self._xcor<=first_dis_column: ### keeping mando on screen
			grid.remove_from_board(self)
			self._xcor+=1

		if direction is 'd':
			if self._xcor < grid_columns-self._columns and self._xcor+5 <last_dis_column:
				grid.remove_from_board(self)
				self._xcor+=3
				return 0
			else: 
				return -1 

		elif direction is 'a':
			if self._xcor > 0 and self._xcor-5 >=first_dis_column:
				grid.remove_from_board(self)
				self._xcor-=5
				return 0
			else:
				self._xcor+=6
				return -1

		elif direction is 'w':
			vel=0

			if self._ycor >= 6: ## 3 because 0th is sky
				grid.remove_from_board(self)
				self._ycor-=5
				return 1
			elif self._ycor > 0 and self._ycor<6:
				grid.remove_from_board(self)
				self._ycor=1
				return 1
			else:
				return -1


		elif direction is 's':
			if self._ycor < grid_rows-1-self._rows:
				grid.remove_from_board(self)
				self._ycor+=3 
				####### now check if y coordinate go out of grid
				if self._ycor > grid_rows-1-self._rows:
					self._ycor = grid_rows-1-self._rows
				return 1
			else:
				return -1

		elif direction is None:
			# if self._xcor<=first_dis_column: ### keeping mando on screen
			# 	grid.remove_from_board(self)
			# 	self._xcor+=1
			if l%2==1:
				vel+=1
			if self._ycor < grid_rows-1-self._rows:##gravity will work and bring him to ground
				grid.remove_from_board(self)
				self._ycor+=vel
				if self._ycor > grid_rows-1-self._rows:
					self._ycor = grid_rows-1-self._rows
				return vel
			if self._ycor == grid_rows-1-self._rows:
				vel=0
				return vel
			else:
				return -1
						
		else:
			return -1


class player(person):

	def __init__(self,xcor,ycor,rows,columns):
		person.__init__(self,xcor,ycor,rows,columns)
		
		self._coins=0	

		for i in range (self._rows): #rows                              
			self.new = []                 
			for j in range (self._columns): #columns  
				self.new.append(" ")      
			self._shape.append(self.new)

		self._shape=[ ['{','^','}'],[' ','|',' '],['/','','\\'] ]

	def magnet_effect(self,display_c1,display_c2,magnet_list):
		x1=self._xcor
		y1=self._ycor	
		### x1->mando_xcor y1->mando_ycor
		### display_c1->first display column of screen 
		### display_c2->last display column of screen
		for i in magnet_list:
			if display_c1<i[0] and i[0]<display_c2: ##magnet is on screen
				if (-30<x1-i[0] and x1-i[0]<30) and (-30<y1-i[1] and y1-i[1]<30): ##range of magnet
					###### changing ycor of mando ######
					if i[1]-y1 < -3:
						self._ycor-=2
					elif i[1]-y1 > 3:
						self._ycor+=2
					elif (i[1]-y1 <= 3) and (i[1] > y1):
						self._ycor=i[1]+4
					elif (i[1]-y1 <= -3) and (i[1] < y1):
						self._ycor=i[1]+4

					#### changing xcor of mando #####
					if i[0]-x1 < -3:
						self._xcor-=2
					elif i[0]-x1 > 3:
						self._xcor+=2
					elif (i[0]-x1 <= 3) and (i[0] > x1):
						self._xcor=i[0]+8
					elif (i[0]-x1 <= -3) and (i[0] < x1):
						self._xcor=i[0]+8

	def shield_activate(self):
		a1 = Fore.GREEN  + '{' + '\x1b[0m'
		a2 = Fore.GREEN  + '^' + '\x1b[0m'
		a3 = Fore.GREEN  + '}' + '\x1b[0m'
		a4 = Fore.GREEN  + '|' + '\x1b[0m'
		a5 = Fore.GREEN  + '/' + '\x1b[0m'
		a6 = Fore.GREEN  + '\\' + '\x1b[0m'

		self._shape=[ [a1,a2,a3],[' ',a4,' '],[a5,' ',a6] ]
	
	def shield_deactivate(self):
		self._shape=[ ['{','^','}'],[' ','|',' '],['/','','\\'] ]
		
	######### mando gets a speed booster   ###########
	def mando_booster_collision(self,store_booster,grid):
		x1=self._xcor
		y1=self._ycor
		r1=self._rows
		c1=self._columns

		for i in store_booster:
			status=i.give_status()
			if status == 0:  ## booster is not taken
				x2=i.give_xcor()
				y2=i.give_ycor()
				r2=i.give_rows()
				c2=i.give_columns()

				check=check_collision(x1,y1,r1,c1,x2,y2,r2,c2)
				if check == 1:

					###remove booster and change its flag	
					i.change_status()
					grid.remove_from_board(i)
					# for m in range(0,3): ##removed booster from grid
					# 	for n in range(0,7):
					# 		matrix[y2+m][x2+n]=' ' 
					return 1

############### MANDALORIAN collects COINS ##############
	def coin_collision(self,coin_list,coins):
		x1=self._xcor
		y1=self._ycor
		r1=self._rows
		c1=self._columns
		for i in coin_list:
			if i[2]==1:
				ans=check_collision(x1,y1,r1,c1,i[0],i[1],1,1)
				if ans==1:
					i[2]=-1 ## change flag for coin
					coins+=1 ##inc no of coins
		return coins

############## MANDALORIAN gets killed #############
	def mando_lazer_collision(self,lazer_list,manga,grid):
		x1=self._xcor
		y1=self._ycor
		r1=self._rows
		c1=self._columns
		
		for i in lazer_list:
			if i[3]==1:
				if i[2]==1:
					ans=check_collision(x1,y1,r1,c1,i[0],i[1],1,5)
					if ans==1:
						lives=manga.decrease_lives() ##decrease mando's lives
						i[3]=-1 ## changing lazer flag
						grid.remove_lazer_from_board(i,1)
						# for k in range(0,5):##remove the lazer from grid
						# 	matrix[i[1]][i[0]+k]=' '
				if i[2]==2:
					ans=check_collision(x1,y1,r1,c1,i[0],i[1],5,1)
					if ans==1:
						lives=manga.decrease_lives() ##decrease mando's lives
						i[3]=-1 ## changing lazer flag
						grid.remove_lazer_from_board(i,2)
						
						# for k in range (0,5): ##remove lazer from grid
						# 	matrix[i[1]+k][i[0]]=' '

				if i[2]==3:
					ans=check_collision(x1,y1,r1,c1,i[0],i[1],5,5)
					if ans==1:
						lives=manga.decrease_lives() ##decrease mando's lives
						i[3]=-1 ## changing lazer flag
						grid.remove_lazer_from_board(i,3)

						# for m in range(0,5): ##remove lazer from grid
						# 	for n in range(0,5):
						# 		matrix[i[1]+m][i[0]+n]=' '

				if i[2]==4:
					ans=check_collision(x1,y1,r1,c1,i[0],i[1],5,5)
					if ans==1:
						lives=manga.decrease_lives() ##decrease mando's lives
						i[3]=-1 ## changing lazer flag
						grid.remove_lazer_from_board(i,4)

						# for m in range(0,5): ##remove lazer from grid
						# 	for n in range(0,5):
						# 		matrix[i[1]+m][i[0]+n]=' '

class enemy(person):
	def __init__(self,xcor,ycor,rows,columns):
		person.__init__(self,xcor,ycor,rows,columns)

		self._lives=10

		with open("./dragon.txt") as obj:
			for line in obj:
				self._shape.append(line.strip('\n'))
		self._rows=len(self._shape)

		self._columns=0
		for i in self._shape:
			if len(i)>self._columns:
				self._columns=len(i)

	def move_enemy(self,manga,grid):
		y1=manga.give_ycor()
		self._ycor=y1-6
		r1=grid.num_rows()
		c1=grid.num_columns()

		if self._ycor <= 0:
			self._ycor = 1

		if self._ycor > r1-1-self._rows:
			self._ycor = r1-1-self._rows


	######## check if bullet hits the enemy ##########
	def bullet_enemy_collision(self,bullet_list,ene,grid):
		x1=self._xcor
		y1=self._ycor
		r1=self._rows
		c1=self._columns

		for i in bullet_list:
			if i[2]==1:  ## bullet is alive
				check=check_collision(x1,y1,r1,c1,i[0],i[1],1,3)
				
				if check==1: ### bullet hit the enemy
					i[2]=-1 ####change the bullet flag
					grid.remove_bullet_from_board(i)
					# for k in range(0,3): ##remove bullet from grid
					# 	matrix[i[1]][i[0]+k]=' '	
					ene.decrease_lives()			

