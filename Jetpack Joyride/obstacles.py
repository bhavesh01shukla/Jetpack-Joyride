from colorama import Fore, Back, Style 
from collisions import check_collision
import board


class obstacles:
	def __init__(self,xcor,ycor,rows,columns):
		self._xcor=xcor
		self._ycor=ycor
		self._rows=rows
		self._columns=columns
	
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

class lazer(obstacles):

	##dont use parent function to copy lazer to grid because of differnt shapes
	##of lazer.Use copy function made for lazer class only 
	def __init__(self,xcor,ycor,rows,columns,pattern_type):
		obstacles.__init__(self,xcor,ycor,rows,columns) ##call parent class
		
		self._pattern_type = pattern_type
		self._laz1 = Fore.YELLOW + Back.RED + '-' + '\x1b[0m'
		self._laz2 = Fore.YELLOW + Back.RED + '|' + '\x1b[0m'
		self._laz3 = Fore.YELLOW + Back.RED + '/' + '\x1b[0m'
		self._laz4 = Fore.YELLOW + Back.RED + '\\' + '\x1b[0m'

	def give_pattern_type(self):
		return self._pattern_type

	def initialize_lazer(self):
		
		if self._pattern_type == 1:
			self._rows=1  ##default row and columns for lazer is 3,3
			self._columns=5
			self._shape=[self._laz1,self._laz1,self._laz1,self._laz1,self._laz1]			
		
		elif self._pattern_type == 2:
			self._rows=5  ##default row and columns for lazer is 3,3
			self._columns=1
			self._shape=[[self._laz2],[self._laz2],[self._laz2],[self._laz2],[self._laz2]]

		elif self._pattern_type == 3:
			self._shape=[[' ',' ',' ',' ',self._laz3],[' ',' ',' ',self._laz3,' '],[' ',' ',self._laz3,' ',' '],[' ',self._laz3,' ',' ',' '],[self._laz3,' ',' ',' ',' ']]

		elif self._pattern_type == 4:
			self._shape=[[self._laz4,' ',' ',' ',' '],[' ',self._laz4,' ',' ',' '],[' ',' ',self._laz4,' ',' '],[' ',' ',' ',self._laz4,' '],[' ',' ',' ',' ',self._laz4]]

		# print(self._rows,self._columns)
	
class magnet(obstacles):
	def __init__(self,xcor,ycor,rows,columns):
		obstacles.__init__(self,xcor,ycor,rows,columns) ##call parent class

		self._north = Fore.BLUE + Back.RED + 'N' + '\x1b[0m'
		self._south = Fore.RED + Back.BLUE + 'S' + '\x1b[0m'

		self._shape=[['-','-','-','-','-','-'],['|',self._north,' ',' ',self._south,'|'],['-','-','-','-','-','-']]
		self._rows=3
		self._columns=6

class coins(obstacles):
	def __init__(self,xcor,ycor,rows,columns):
		obstacles.__init__(self,xcor,ycor,rows,columns) ##call parent class

		self._shape = Fore.YELLOW + '\033[01m' + '$' + '\x1b[0m'		
			
class booster(obstacles):
	def __init__(self,xcor,ycor,rows,columns):
		obstacles.__init__(self,xcor,ycor,rows,columns) ##call parent class

		self._sb1 = Fore.CYAN + 'B' + '\x1b[0m'
		self._sb2 = Fore.CYAN  + 'O' + '\x1b[0m'
		self._sb3 = Fore.CYAN  + 'O' + '\x1b[0m'
		self._sb4 = Fore.CYAN  + 'S' + '\x1b[0m'
		self._sb5 = Fore.CYAN + 'T' + '\x1b[0m'

		self._rows=3
		self._columns=7

		self._shape = [['-','-','-','-','-','-','-'],['|',self._sb1,self._sb2,self._sb3,self._sb4,self._sb5,'|'],['-','-','-','-','-','-','-']]
		self._status=0  ##is the boost taken by mando
	
	def give_status(self):
		return self._status
	
	def change_status(self):
		self._status=1



class bullets:
	def __init__(self,xcor,ycor,rows,columns):

		self._chr = Fore.BLACK + Back.RED + 'O' + '\x1b[0m'
		self._shape=[self._chr,self._chr,self._chr]	
		
		self._xcor=xcor
		self._ycor=ycor
		self._rows=1
		self._columns=3


class ice_balls:
	def __init__(self,xcor,ycor):

		self._xcor=xcor
		self._ycor=ycor
		self._rows=1
		self._columns=2

		self._chr = Fore.BLACK + Back.CYAN + 'O' + '\x1b[0m'
		self._shape=[self._chr,self._chr,self._chr]	
		self._alive=1

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

	def ice_ball_status(self):
		return self._alive

	def move_ice_balls(self,first_display_column):
		self._xcor-=1
		if self._xcor <= first_display_column:
			self._alive = 0

	def kill_mando(self,manga):
		if self._alive==1: ##only if the ice_ball is alive and in the screen 
			x1=manga.give_xcor()
			y1=manga.give_ycor()
			r1=manga.give_rows()
			c1=manga.give_columns()

			check=check_collision(x1,y1,r1,c1,self._xcor,self._ycor,self._rows,self._columns)
			if check==1:##ice_ball hit mando
				self._alive=0 ###bullet is now dead
				manga.decrease_lives() ###decrease lives
			

	def ice_bullet_collision(self,bullet_list,grid):
		for i in bullet_list:
			if i[2]==1: ##bullet is alive
				check=check_collision(self._xcor,self._ycor,self._rows,self._columns,i[0],i[1],1,3)
				if check==1:
					self._alive=0 ##change both flags
					i[2]=-1
					###remove bullet
					grid.remove_bullet_from_board(i)
					###remove ice ball
					grid.remove_ice_balls_from_board(self)

				
