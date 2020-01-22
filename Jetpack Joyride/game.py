from colorama import Fore, Back, Style 
from input import Get, input_to
import os
import sys
import random
import time

from board import Board
from mandalorian import person,enemy,player
from obstacles import obstacles,lazer,magnet,coins,booster,bullets,ice_balls
from collisions import check_collision

lazer_list=[]
magnet_list=[]
coin_list=[]
bullet_list=[]
booster_list=[]
ice_ball_list=[]


store_magnets=[]
store_lazer=[]
store_booster=[]

				
def make_coins_for_given_xy(x,y):
	columns=5
	rows=2
	for i in range (0,columns):
		for j in range (0,rows):
			temp=coins(x+i,y+j,1,1)
			grid.copy_coins_on_board(temp) ###copying coins on board
			new=[x+i,y+j,1] ##1 is the flag that coin is present
			coin_list.append(new)


#############  INITIALIZING GRID #############
grid=Board(40,1000)
grid.initialize_background()

r=grid.num_rows()
c=grid.num_columns()
# print(r,c)


############## MAKING COINS   ##############
#####no of coins will be made in swaure matrix of 4
for i in range (0,50):
	y_position=random.randrange(7,32,1)
	x_position=random.randrange(20,800,1)
	
	make_coins_for_given_xy(x_position,y_position)

	
#################  	MAKING LAZER BEAMS ####################
for i in range (0,25):
	a=random.choice([1,2,3,4])
	y_position=random.randrange(8,32,1)
	x_position=random.randrange(20,750,1)
	b=lazer(x_position,y_position,5,5,a) ## flag 1 means lazer is active
	store_lazer.append(b)

	new=[x_position,y_position,a,1] ## a->lazer_type 
	lazer_list.append(new)

	b.initialize_lazer()
	grid.copy_on_board(b)


########### MAKING MAGNETS   #############################
for i in range (0,3):
	y_position=random.randrange(8,32,1)
	x_position=random.randrange(100,600,1)

	new=[x_position,y_position,1]  ##1 is the flag that magnet is on right side
	magnet_list.append(new)

	mag1=magnet(x_position,y_position,3,6)
	store_magnets.append(mag1)
	grid.copy_on_board(mag1)

############## MAKING MANDALORIAN ##############
manga = player(10,5,3,3) ##give y coordinate=y_grid_size-1 
grid.copy_player_on_board(manga)

######### MAKING ENEMY ##############
ene=enemy(900,3,3,3)
grid.copy_on_board(ene)

######### MAKING SPEED BOOSTER   #########
for i in range(0,10):
	y_position=random.randrange(8,32,1)
	x_position=random.randrange(20,750)

	new=[x_position,y_position,1]  ##1 is the flag that booster is not taken
	booster_list.append(new)

	boo1=booster(x_position,y_position,3,7)
	store_booster.append(boo1)
	grid.copy_on_board(boo1)

getch=Get()
cnt=0
speed_counter=0
old_time=time.time()
waste=0
wait_time=0.1
shield_available=0
shield_last_disabled=old_time
shield_activated_at=old_time
flag=0 ### if flag is 0 check mando-lazer collision
m_dead=0
e_dead=0
l=0
vel=0
game_start_time=int(time.time())
finish_game=0

while True:

	if speed_counter < 0:
		speed_counter=0

	print("\033[0;0f",end="")
	input=input_to(getch)

	### this while loop is like sleep function
	if wait_time!=0:
		while (time.time() - old_time < wait_time):
			waste+=1
	if (150+game_start_time-time.time()<0):
		finish_game=1
		break
	
	#####enable shield
	if (time.time() - shield_last_disabled > 5 and flag==0 ):
		shield_available=1

	####disable shield
	if (time.time() - shield_activated_at > 10 and flag==1):
		shield_available=0
		shield_last_disabled=time.time()
		flag=0
		manga.shield_deactivate()

	os.system('clear')
		
	if input is 'q':
		os.system('clear')
		sys.exit()	
	elif input is ' ':  ## activate shield if present
		if shield_available == 1:
			shield_activated_at=time.time()
			flag=1 #### dont check mando-lazer collision
						
	elif input is 'b':  ### fire a bullet
		x=manga.give_xcor()
		y=manga.give_ycor()
		bul=bullets(x+2,y,1,3)
		temp=[x,y,1] ## here 1 is the flag that bullet is live 
		bullet_list.append(temp)
	else:
			vel=manga.movement_possible(input,r,c,cnt,cnt+100,l,vel,grid)
			if vel<= 0: ####checking velocity value
				vel=0
	
	#####copy magnets on board ######
	for i in store_magnets:
		grid.copy_on_board(i)		

	####### check collisions with coins ######### 	
	num_coins=manga.give_coins()
	coins=manga.coin_collision(coin_list,num_coins)
	manga.update_coins(coins)

		
	####### collision of mandalorian with lazers ####
	if flag==0:
		manga.mando_lazer_collision(lazer_list,manga,grid)
		
	# grid.copy_player_on_board(manga)

	########## handling bullets ###############
	grid.bullet_out_of_range(bullet_list,cnt+100)
	grid.remove_bullets_from_board(bullet_list)
	grid.reposition_bullet_coordinates(bullet_list)
	grid.copy_bullets_on_board(bullet_list)
	

	grid.bullet_lazer_collision(bullet_list,lazer_list)

	grid.remove_from_board(manga)
	manga.magnet_effect(cnt,cnt+100,magnet_list)
	# grid.copy_player_on_board(manga)

	#######remove ice balls from board######
	for i in ice_ball_list:
		st=i.ice_ball_status()
		if st==1:
			grid.remove_ice_balls_from_board(i)

	######## move ice balls  ##########
	for i in ice_ball_list:
		i.move_ice_balls(cnt)

	###### bullet-ice ball collision #####
	for i in ice_ball_list:
		st=i.ice_ball_status()
		if st==1:  ###ice ball is alive
			i.ice_bullet_collision(bullet_list,grid)

	####### mando_ice-ball_collision #####
	if  flag==0: 
		for i in ice_ball_list:
			st=i.ice_ball_status()
			if st==1:
				i.kill_mando(manga)
				m_lives=manga.give_lives()
				if m_lives<=0: ###mando is dead
					m_dead=1
					break
	
	#######copy ice balls on board ######
	for i in ice_ball_list:
		grid.copy_ice_balls_on_board(i)	

	#####  bullet enemy collision ##########
	xe=ene.give_xcor()
	ye=ene.give_ycor()
	re=ene.give_rows()
	ce=ene.give_columns()	
	ene.bullet_enemy_collision(bullet_list,ene,grid)

	######   check if enemy is dead  #########
	e_lives=ene.give_lives()
	if e_lives <= 0:
		e_dead=1
		break  #### break the loop and print 'win'


	########check if mando is dead ###########	
	m_lives=manga.give_lives()
	if m_lives<=0: ###mando is dead
		m_dead=1
		break
	##########################################

	clash=manga.mando_booster_collision(store_booster,grid)
	if clash==1:
		speed_counter=100

	if flag==1: ###shield is being used,color mando green
		manga.shield_activate()
	# elif flag==0: ###shield is not being used
	grid.copy_player_on_board(manga)

	grid.remove_from_board(ene)
	ene.move_enemy(manga,grid)
	grid.copy_on_board(ene)


	#####   enemy fires ice balls  ########
	x_m=manga.give_xcor()
	y_m=manga.give_ycor()
	x_e=ene.give_xcor()
	y_e=ene.give_ycor()

	##### enemy fires ice balls on mando ########
	if x_e-x_m <=80:
		if y_m-2<= 0: ####if ycor of ice ball goes out of screen
			ball=ice_balls(x_e-1,y_m)
			ice_ball_list.append(ball)
		else:
			ball=ice_balls(x_e-1,y_m-2)
			ice_ball_list.append(ball)
	#######################################	

	grid.print_board(cnt,39,manga,shield_available,flag,shield_last_disabled,game_start_time)

	if(speed_counter>0):
		# time.sleep(0.00001)
		wait_time=0
		speed_counter-=1
	else:
		# time.sleep(0.1)
		wait_time=0.1	

	if cnt < 850: ####position of dragon,screen freezes
		cnt+=1
	l+=1
	old_time=time.time()

os.system('clear')
if finish_game==1:
	print('Time Over')
	print('You lose')

if m_dead==1:
	print('You lose')
	quit()

if e_dead==1:
	print('You won')
	quit()