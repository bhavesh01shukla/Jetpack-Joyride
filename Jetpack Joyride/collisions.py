
def check_collision(x1,y1,r1,c1,x2,y2,r2,c2):
	if (x1<=x2 and x2<=x1+c1) and (y1<=y2+r2 and y2+r2<=y1+r1):
		return 1
	
	elif (x1<=x2 and x2<=x1+c1) and  (y1<=y2 and  y2<=y1+r1):
		return 1
	
	elif (x2<=x1) and(x1+c1<=x2+c2) and (y2<=y1+r1 and y1+r1<=y2+r2):
		return 1	

	elif (y1<=y2 and y2<=y1+r1) and (x1<=x2) and (x2+c2<=x1+c1):
		return 1	

	elif (y2<=y1) and (y1+r1<=y2+r2) and (x1<=x2 and x2<=x1+c1):
		return 1	

	elif (y1<=y2) and (y2+r2<=y1+r1) and (x1<=x2 and x2<=x1+c1):
		return 1	

	elif (x1<=x2) and (x1+c1>=x2+c2) and (y1<=y2) and (y2+r2<=y1+r1):
		return 1	
		
	elif (x1<=x2) and (x1+c1>=x2+c2) and (y2<=y1) and (y1+r1<=y2+r2):
		return 1	

	else:
		return -1	
