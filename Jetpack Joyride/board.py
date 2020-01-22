from colorama import Fore, Back, Style 
from collisions import check_collision
from mandalorian import person,player,enemy
from obstacles import obstacles,lazer,magnet,coins,booster,bullets,ice_balls
import time


class Board:
	'''This class creates the grid for the game, and displays it'''
	
	def __init__(self, rows, columns): # initialize values
		self._rows=rows
		self._columns=columns
		self._matrix=[]
		self._ground=Fore.YELLOW + "T" + '\x1b[0m'
		self._sky = Fore.CYAN + "X" + '\x1b[0m'

		for i in range (0,self._rows):
			temp=[]
			for j in range (0,self._columns):
				temp.append(" ")
			self._matrix.append(temp)

	def num_rows(self):
		return self._rows

	def num_columns(self):
		return self._columns


	def initialize_background(self): # creates the entire grid

		for i in range (0,self._columns):
			self._matrix[self._rows-1][i]=self._ground ##making ground
			self._matrix[0][i]=self._sky  ##making sky

	def copy_on_board(self,object):
		shape=object.give_shape()
		x=object.give_xcor()
		y=object.give_ycor()
		r=object.give_rows()
		c=object.give_columns()

		if r==1:
			for i in range(0,c):
				self._matrix[y][x+i]=shape[i]

		else:
			for i in range (0,r):
				for j in range(0,c):
					self._matrix[y+i][x+j]=shape[i][j]

	def remove_from_board(self,object):
		shape=object.give_shape()
		x=object.give_xcor()
		y=object.give_ycor()
		r=object.give_rows()
		c=object.give_columns()
		shape=object.give_shape()
		if r==1:
			for i in range(0,c):
				self._matrix[y][x+i]=' '

		else:
			for i in range (0,r):
				for j in range(0,c):
					self._matrix[y+i][x+j]=' '
		
	def print_board(self,xstart,yend,manga,shield_available,flag,t2,t3):
		coins=manga.give_coins()
		lives=manga.give_lives()

		
		xend=xstart+100
		for i in range (0,yend+1):
				for j in range (xstart,xend+1):
					print(self._matrix[i][j],end="")
				print()
		print("Coins:",coins,end='\t\t\t')
		print("Lives left:",lives)

		if shield_available==0:
			print("Shield available:NO",end='\t\t')
		else:
			print("Shield available:YES",end='\t\t')
		
		if flag==0:
			print("Shield activated:NO")
			a=int(5-time.time()+t2)
			if a>=0:
				print("Shield coming in:",int(5-time.time()+t2))
		else:
			print("Shield activated:YES")

		print('Time left:',150+t3-int(time.time()))		


	######### BULLET destroys lazer ############
	def bullet_lazer_collision(self,bullet_list,lazer_list):
		for i in bullet_list:
			if i[2]==1: ##bullet is alive
				for j in lazer_list:
					
					if j[3]==1 and j[2]==1:  ##horizontal lazer
						ans=check_collision(i[0],i[1],1,3,j[0],j[1],1,5)
						if ans==1:
							##remove the lazer and kill the bullet
							i[2]=-1	##bullet flag changed
							j[3]=-1  ##lazer dead,flag changed
							
							for k in range(0,5):##remove the lazer from grid
								self._matrix[j[1]][j[0]+k]=' '	

							for k in range(0,3): ##remove bullet from grid
								self._matrix[i[1]][i[0]+k]=' ' 


					if j[3]==1 and j[2]==2:  ##vertical lazer
						ans=check_collision(i[0],i[1],1,3,j[0],j[1],5,1)
						if ans==1:
							i[2]=-1 ##bullet flag changed
							j[3]=-1  ##lazer dead,flag changed

							for k in range (0,5): ##remove lazer from grid
								self._matrix[j[1]+k][j[0]]=' '
							for k in range(0,3): ##remove bullet from grid
								self._matrix[i[1]][i[0]+k]=' ' 

					if j[3]==1 and j[2]==3:  ## diagonal lazer
						ans=check_collision(i[0],i[1],1,3,j[0],j[1],5,5)
						if ans==1:
							i[2]=-1 ##bullet flag changed
							j[3]=-1  ##lazer dead,flag changed
							
							for m in range(0,5): ##remove lazer from grid
								for n in range(0,5):
									self._matrix[j[1]+m][j[0]+n]=' ' 
							for k in range(0,3): ##remove bullet from grid
								self._matrix[i[1]][i[0]+k]=' ' 

					if j[3]==1 and j[2]==4:  ## diagonal lazer
						ans=check_collision(i[0],i[1],1,3,j[0],j[1],5,5)
						if ans==1:
							i[2]=-1 ##bullet flag changed
							j[3]=-1  ##lazer dead,flag changed
							
							for m in range(0,5): ##remove lazer from grid
								for n in range(0,5):
									self._matrix[j[1]+m][j[0]+n]=' ' 
							for k in range(0,3): ##remove bullet from grid
								self._matrix[i[1]][i[0]+k]=' ' 


	######### Pasting new position of bullets on grid ############
	def copy_bullets_on_board(self,bl):
		ch = Fore.BLACK + Back.RED + 'O' + '\x1b[0m'
		## i[0]=xcor ,i[1]=ycor
		if len(bl) > 0:
			for i in bl:
				if i[2] != -1:
					for j in range (0,3):
						self._matrix[i[1]][i[0]+j] = ch

	######### Removing trajectory of a bullet #########
	def remove_bullets_from_board(self,bl):
		## i[0]=xcor ,i[1]=ycor
		if len(bl) > 0:
			for i in bl:
				if i[2] != -1:
					for j in range (0,3):
						self._matrix[i[1]][i[0]+j] = " "

	####### Finding new coordinates of live bullets ##########
	def reposition_bullet_coordinates(self,bl):  ## bl means bullet_list
		### moving all available bullets
		## i[0]=xcor ,i[1]=ycor
		if len(bl) > 0:
			for i in bl:
				if i[2] != -1:
					i[0]+=3  ####speed of bullet

	######### kill the bullets that go out of screen #########
	def bullet_out_of_range(self,bl,last_column):
		if len(bl) > 0:
			for i in bl:
				if i[0] >=last_column-2:
					for j in range (0,3):
						self._matrix[i[1]][i[0]+j] = " "
					i[2]=-1


	def copy_player_on_board(self,manga):
		shape=manga.give_shape()
		x=manga.give_xcor()
		y=manga.give_ycor()
		r=manga.give_rows()
		c=manga.give_columns()

		for i in range (0,r):
			for j in range (0,c):
				self._matrix[y+i][x+j]=shape[i][j]


	def remove_bullet_from_board(self,i):
		for k in range(0,3): ##remove bullet from grid
			self._matrix[i[1]][i[0]+k]=' '	

	def remove_lazer_from_board(self,i,pattern):
		if pattern==1:
			for k in range(0,5): ##remove bullet from grid
				self._matrix[i[1]][i[0]+k]=' '	
		elif pattern==2:
			for k in range(0,5):
				self._matrix[i[1]+k][i[0]]=' '
		elif pattern==3 or pattern==4:
			for m in range(0,5):
				for n in range(0,5):
					self._matrix[i[1]+m][i[0]+n]=' '

	def copy_lazer_on_board(self,i):
		pattern=i.give_pattern_type()
		x=i.give_xcor()
		y=i.give_ycor()
		shape=i.give_shape()

		if pattern==1:
			for k in range(0,5): ##remove bullet from grid
				self._matrix[y][x+k]=shape[k]
		else:
			for m in range(0,5):
				for n in range(0,5):
					self._matrix[y+m][x+n]=shape[m][n]
	
	def remove_ice_balls_from_board(self,i):
		x=i.give_xcor()
		y=i.give_ycor()
		for k in range(0,3): ##remove ice-ball from grid
				self._matrix[y][x+k]=' '

	def copy_ice_balls_on_board(self,ball):
		check=ball.ice_ball_status()
		x=ball.give_xcor()
		y=ball.give_ycor()
		r=ball.give_rows()
		c=ball.give_columns()
		shape=ball.give_shape()
		if check == 1:
			for j in range (0,c):
				self._matrix[y][x+j] = shape[j] 

	def copy_coins_on_board(self,i):
		laz1 = Fore.YELLOW + Back.RED + '-' + '\x1b[0m'
		laz2 = Fore.YELLOW + Back.RED + '|' + '\x1b[0m'
		laz3 = Fore.YELLOW + Back.RED + '/' + '\x1b[0m'
		laz4 = Fore.YELLOW + Back.RED + '\\' + '\x1b[0m'

		x=i.give_xcor()
		y=i.give_ycor()
		r=i.give_rows()
		c=i.give_columns()
		shape=i.give_shape()
		te=self._matrix[y][x]
		if te!=laz1 and te!=laz2 and te!=laz3 and te!=laz4:
			self._matrix[y][x]=shape

