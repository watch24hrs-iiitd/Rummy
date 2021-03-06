# TASKS
# GAME FINISHED! NO TASKS LEFT
#____________________________________________________________________________________________________________________________________________________________________________________

import sys, pygame, random, time, colorama, datetime
from matplotlib import pyplot as plt
import numpy as np
from termcolor import colored
from pygame.locals import *
from itertools import chain

class user:
	def __init__(self,name='User'):
		'''
		DATA MEMBERS:
		NAME 
		CARDS
		DICT OF CARDS
		POSITION OF CARDS # nested list of top_left,bottom_right
		JOKER #2nd Joker
		'''
		self.name=name
		self.cards=None # overwrite in choose_cards
		self.cardsDict=None # overwrite in choose_cards
		self.cardsPos=[]
		self.joker2=None
		self.welcome()

	def welcome(self):
		
		colorama.init()
		print()
		colors = ['red','green','cyan','magenta','white','blue','yellow']
		for i in range(72):
			print(colored('=',random.choice(colors)),end='')
		print()
		print(colored('Welcome to Indian Rummy!','yellow'))
		sprint('Enter your name: ')
		string=input()
		self.name=string
		print()
	
	def dict_cards(self):
		d={}
		for i in self.cards:
			d[i]=False 
		self.cardsDict=d
		
	def choose_cards(self):
		
		suits=['C','D','H','S'] #suits
		values=[] #values of cards
		for i in range(1,15):
			values.append(str(i)) # value 14 is used for joker
		cards=[]
		i=0
		while i<13:
			(val,suit) = (random.choice(values),random.choice(suits))
			addCard = val + suit
			if cards.count(addCard)<1: 
				cards.append(addCard)
				i+=1

		(val,suit) = (random.choice(values),random.choice(suits))
		addCard = val + suit
		joker_chosen = False
		while not joker_chosen:
			if (cards.count(addCard)<1) and (addCard[:-1]!='14'):
				self.joker2 = addCard #intitialise the second joker here
				joker_chosen = True

		#OVERWRITING THE CARDS FOR TEST PURPOSES
		# cards = ['1S','2S','3S','4S','5S','6S','7S','8S','9S','10S','11S','12S','13S'] # sequence 
		# cards = ['1S','2S','3S','4S','5S','6S','7S','8S','14S','10S','11S','12S','13S'] # sequence with joker
		# cards = ['1S','2S','3S','4S','5S','13H','7S','8S','14S','8C','11S','11C','11H'] # sequence with joker and set 
		
		#OVERWRITING THE CARDS FOR TEST PURPOSES
		#self.joker2 = '13D'

		self.cards=cards # cards assigned to the object
		self.dict_cards() # dictionary created of cards

	def display_cards(self,screen,y=510,submit=False):
		if submit: # if the game is submitted refresh the card pos 
			self.cardsPos=[] 
		cards=self.cards
		for i in range(len(cards)):
			card = pygame.image.load('Cards/patte/'+cards[i]+'.jpg')
			card = pygame.transform.scale(card,card_scale)
			pos_top_left=(30+110*i,y) #position set through direct values 
			pos_bottom_right=(pos_top_left[0]+card_scale[0],pos_top_left[1]+card_scale[1])
			(range(pos_top_left[0],pos_bottom_right[0]),range(pos_top_left[1],pos_bottom_right[1]))
			if len(self.cardsPos) != 13: #only need position for the first iteration
				self.cardsPos.append((pos_top_left,pos_bottom_right))
			screen.blit(card,pos_top_left)
			# condition if a card is selected
			if list(self.cardsDict.values())[i]:
					pygame.draw.circle(screen,(255,0,0),self.cardsPos[i][0],6)
	
	def Card_chosen(self,i):
			self.cardsDict[self.cards[i]] = not (self.cardsDict[self.cards[i]])

	def check_cursor(self,mouse_pos):
		for i in range(len(self.cardsPos)):
			x=range(self.cardsPos[i][0][0],self.cardsPos[i][1][0])
			y=range(self.cardsPos[i][0][1],self.cardsPos[i][1][1])
			if (mouse_pos[0] in x) and (mouse_pos[1] in y):
				return (True, i) # Tuple boolean and index
		return (False,-1)

	def swap_cd(self):
		global cards_drawn
		global select_cd_card
		global move_count
		global called_cd_card
		j=0
		for i in self.cardsDict.values():
			if i:
				swap_sound.play()
				(self.cards[j],cards_drawn[-1])=(cards_drawn[-1],self.cards[j])
				self.dict_cards()
				select_cd_card = False
				move_count +=1 #as a move is made
				called_cd_card = False #a move is made, (safe logic)
				return True
			j+=1
		return False

	def swap(self):
		val=list(self.cardsDict.values())
		if val.count(True)==2:
			swap_sound.play()
			i1=val.index(True)
			i2=val.index(True,i1+1)
			(self.cards[i2],self.cards[i1])=(self.cards[i1],self.cards[i2])
			self.dict_cards()

# saves an image of the highscore
def plot_scores():
	#data obtained from highscore file
	f = open('highscore.txt','r')
	scores = list(f)
	for i in range(len(scores)):
		scores[i] = scores[i].split()
	scores = sorted(scores, key = lambda x:int(x[1]),reverse = False)
	f.close()
	#top 3 scores
	scores = scores[:5]

	mc = []
	names = []
	for i in scores:
		mc.append(int(i[1]))
		names.append(i[0])

	fig, ax = plt.subplots()
	index = np.arange(5)
	bar_width = 0.35
	opacity = 0.8

	rects1 = plt.bar(index + bar_width, tuple(mc), bar_width,
	alpha=opacity,
	color='r',)

	plt.title('Highscores!')
	plt.xlabel('Player -->')
	plt.ylabel('Move Count -->')
	plt.xticks(index + bar_width, tuple(names))
	path = 'highscore.jpg'
	plt.savefig(path,bbox_inches='tight')

#running text
def sprint(s):
	typing_speed = 95 #wpm
	def slow_type(t):
		for l in t:
			sys.stdout.write(l)
			sys.stdout.flush()
			time.sleep(random.random()*10.0/typing_speed)
		print()
	slow_type(s)

def display_joker(card,X=95,Y=175):
	
	def display_msg(x):
		def text_objects(x,font):
			textSurface = font.render(x, True , (255,255,255))
			return textSurface, textSurface.get_rect()
		text = pygame.font.SysFont('Comic Sans MS',25)
		textSurf, textRect = text_objects(x, text)
		textRect.center = (X,Y)
		screen.blit(textSurf, textRect)
	
	display_msg('Wildcard')
	a = pygame.image.load('Cards/patte/'+card+'.jpg')
	a = pygame.transform.scale(a,card_scale)
	screen.blit(a,(50,200))

#return a random card from closed deck
def closed_deck_card(cards):
	suits=['C','D','H','S'] #suits
	values=[] #values of cards
	for i in range(1,15):
		values.append(str(i))
	check=True
	while check:
		(val,suit) = (random.choice(values),random.choice(suits))
		card = val + suit
		if (cards.count(card)<1) and (card not in cards_drawn): 
			check = False
			cards_drawn.append(card)
			return cards_drawn
		
def shuffle_for_comp():
	global u
	suits=['C','D','H','S'] #suits
	values=[] #values of cards
	for i in range(1,15):
		values.append(str(i)) # value 14 is used for joker
	cards=[]
	i=0
	while i<13:
		(val,suit) = (random.choice(values),random.choice(suits))
		addCard = val + suit
		if (cards.count(addCard) == 0) and (addCard not in u.cards): 
			cards.append(addCard)
			i+=1
	return cards


def comp_win():

	global u
	global comp_win_var
	#overwriting for checking purposes
	u.cards = comp_cards

	l = []
	for i in range(1,14):
		l.append(i)
	
	def evaluate_comp(l1,l2,l3,l4,l3_choice,l4_choice):
		
		def reduceBy1(l): # as for user, 0 card is 1st card 
			for i in range(len(l)):
				l[i]-=1

		reduceBy1(l1)
		reduceBy1(l2)
		reduceBy1(l3)
		reduceBy1(l4)

		def cards_num_check(l1,l2,l3,l4):
			l=[]
			l.append(l1)
			l.append(l2)
			l.append(l3)
			l.append(l4)
			a=sorted(l,key = lambda x:len(x))
			if (len(a[0]) == 3) and (len(a[1]) == 3) and (len(a[2]) == 3) and (len(a[3]) == 4):
				return True
			else:
				return False

		def check1(l):
			for i in l:
				if l.count(i)>1:
					return False
			return True

		def check2(l):
			checklist=[]
			suit=[]
			for i in l:
				if u.cards[i][:-1] == '14': #joker detected
					return False
				else:
					checklist.append(int(u.cards[i][:-1]))
					suit.append(u.cards[i][-1])
			
			#all suits should be the same
			if suit.count(suit[0])!=len(l):
				return False
			
			checklist=sorted(checklist)
			check = True
			for i in range(len(checklist)-1):
				if checklist[i+1]-checklist[i]==1:
					check = check and True
				else:
					check = check and False
			return check

		def check3(l):
			checklist=[]
			suit=[]
			for i in l:
				checklist.append(int(u.cards[i][:-1]))
				suit.append(u.cards[i][-1])
			if checklist.count(14)>=2:
				return False
			if not((suit.count(suit[0]) == len(l)) or (suit.count(suit[0]) == len(l)-1) or (suit.count(suit[1]) == len(l)) or (suit.count(suit[1]) == len(l)-1)):
				return False
			check = True
			checklist = sorted(checklist)
			for i in range(len(checklist)-2):
				if checklist[i+1]-checklist[i]==1:
					check = check and True
				elif checklist[i+1]-checklist[i]==2:
					if checklist[-1] == 14:
						check = check and True
					else:
						check = check and False
				else:
					check = check and False
			return check

		def check4(l,sequence):
			if sequence:
				return check3(l)
			else:
				def set_check(cards):
					check = True
					key = cards[0][:-1]
					for i in cards:
						if i[:-1] == key:
							check = check and True
						else:
							check = check and False
					return check
				#check for set 
				cards=[]
				joker_count = 0 
				for i in l:
					if u.cards[i][:-1] == '14':
						joker_count+=1
					cards.append(u.cards[i])
				if joker_count>1:
					return False
				cards = sorted(cards,key = lambda x:int(x[:-1]))
				if int(cards[-1][:-1]) == 14: #joker is present 
					cards = cards[:-1]
				return set_check(cards)

		l=l1+l2+l3+l4
		if not(sorted(l) == [0,1,2,3,4,5,6,7,8,9,10,11,12]):
			return False
		if not(cards_num_check(l1,l2,l3,l4)):
			return False
		if not(check1(l)):
			return False
		if not(check2(l1)):
			return False
		if not(check3(l2)):
			return False
		if not(check4(l3,l3_choice)):
			return False
		if not(check4(l4,l4_choice)):
			return False
		
		return True 
	
	win = False
	for l3_choice in range(0,2):
		for l4_choice in range(0,2):
			win = win or evaluate_comp(l[:5],l[5:8],l[8:11],l[11:],bool(l3_choice),bool(l4_choice)) 
			win = win or evaluate_comp(l[:4],l[4:8],l[8:11],l[11:],bool(l3_choice),bool(l4_choice)) 
			win = win or evaluate_comp(l[:4],l[4:7],l[7:11],l[11:],bool(l3_choice),bool(l4_choice)) 
			win = win or evaluate_comp(l[:4],l[4:7],l[7:10],l[10:],bool(l3_choice),bool(l4_choice)) 

	if win:
		comp_win_var = True

def comp_move(comp_cards,cards_drawn):
	global u
	by_var = u.cards
	comp_win()
	u.cards = by_var
	by_cards = comp_cards
	yes = []
	for i in range(len(comp_cards)):
		x = (comp_move_f(comp_cards[:i]+[cards_drawn[-1]]+comp_cards[i+1:]),i)
		yes.append(x)
	yes = sorted(yes, key = lambda x:x[0][0]+x[0][1],reverse = True)
	(comp_cards[yes[-1][-1]],cards_drawn[-1]) = (cards_drawn[-1],comp_cards[yes[-1][-1]])
	comp_cards = yes[-1][0][2]
	return (cards_drawn,comp_cards)

def comp_move_f(comp_cards):	
	def sort_cards(comp_cards):
		suits=['C','D','H','S'] #suits
		l=[[],[],[],[]]
		for i in comp_cards:
			if i[-1] in suits:
				l[suits.index(i[-1])].append(i)
		for i in range(len(l)):
			l[i] = sorted(l[i], key = lambda x:int(x[:-1]))
		return l
	
	def set_cards_function(comp_cards):
		set_cards = sorted(comp_cards, key = lambda x:int(x[:-1])) # (1H,3H,2D,1D) -> (1H,1D,2D,3H)
		l = []
		for j in range(14):
			l.append([])
		for i in set_cards:
			l[int(i[:-1])-1].append(i) #each card is appended to its integer position - 1
		return l

	set_cards = set_cards_function(comp_cards)	
	sequence_cards = sort_cards(comp_cards)

	def get_l_sequences(l):
		x=[]
		suit = l[0][-1]
		for j in l:
			x.append(int(j[:-1]))
		l=x
		a = [[]]
		i=0
		count=0
		while i<len(l):
			subcount=0
			for j in range(i,len(l)):
				if (l[j]-l[i]) == (j-i):
					if subcount>=4:
						break
					a[count].append(l[j])
					subcount+=1
			count+=1
			a.append([])
			i+=len(a[count-1])
		b = []
		for i in a:
			if not(len(i)<=1):
				b.append(i)
		for i in range(len(b)):
			for j in range(len(b[i])):
				b[i][j] = str(b[i][j])+suit
		return b

	seq_formed = []
	for i in sequence_cards:
		if i!=[]:
			seq_formed.append(get_l_sequences(i))
	seq_formed = [j for sub in seq_formed for j in sub]
	seq_formed_flatten_list = [j for sub in seq_formed for j in sub] 
	seq_number = len(seq_formed)
	set_cards_final = []
	for i in set_cards:
		check = True
		for j in i:
			if j in seq_formed_flatten_list:
				check = check and False
		if check:
			set_cards_final.append(i)
	set_number = len(set_cards_final)
	set_cards_final_flatten = [j for sub in set_cards_final for j in sub]
	final_comp_cards = seq_formed_flatten_list + set_cards_final_flatten
	for i in comp_cards:
		if i not in final_comp_cards:
			final_comp_cards.append(i)
	return (seq_number,set_number,final_comp_cards)

def comp_move1(cards_drawn,u):
	suits=['C','D','H','S'] #suits
	values=[] #values of cards
	for i in range(1,15):
		values.append(str(i))
	check = True
	while check:
		(val,suit) = (random.choice(values),random.choice(suits))
		card = val + suit
		if (card not in u.cards) and (card not in cards_drawn): # and not in comp_cards
			cards_drawn.append(card)
			return cards_drawn
			check = False

def comp_win1():
	global move_count
	win_move = int(random.uniform(10,13))
	if int(move_count/2) == win_move:
		lose_1()

def lose_1():
	colorama.init()
	pygame.mixer.music.stop()
	print(colored('COMP WINS','yellow'))
	print(colored('COMP CARDS: '+str(comp_cards)),'blue')
	print(colored('You lose :(','red'))
	print()
	lose_sound.play()
	time.sleep(5)
	print('BYE!')
	sys.exit()

cards_drawn = [] #cards drawn 

u=user()

#distributing cards
u.choose_cards()
comp_cards = shuffle_for_comp()
#overwriting for test_purposes
#comp_cards = ['1S','2S','3S','4S','5S','14H','7S','8S','14S','8C','11S','11C','11H']
comp_win_var = False

#highscore img loading
plot_scores() 

loading_screen = True # to be displayed 

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
pygame.display.set_caption('Hi ' + u.name + '!')

screen_size = (width,height) = (1500,700)
card_scale = (100,160)
screen_size_minimize = (1500,300)

screen = pygame.display.set_mode(screen_size)

bg_start = pygame.image.load('bg/bg_start.jpg')
bg_start = pygame.transform.scale(bg_start,screen_size)

call_closed_card_count = False # for first iteration
select_cd_card = False

cursor_value = (False,-1)

submit = False # for submitting user cards

in_game = True

#sound effects
pygame.mixer.music.load('sounds/bg.wav')
nope_sound = pygame.mixer.Sound('sounds/nope.wav')
start_sound = pygame.mixer.Sound('sounds/start.wav')
click_sound = pygame.mixer.Sound('sounds/c.wav')
submit_sound = pygame.mixer.Sound('sounds/s.wav')
swap_sound = pygame.mixer.Sound('sounds/swap.wav')
clock_sound = pygame.mixer.Sound('sounds/clock.wav')
ping_sound = pygame.mixer.Sound('sounds/ping.wav')
lose_sound = pygame.mixer.Sound('sounds/lose.wav')
pygame.mixer.music.play(-1)

move_count = 0 #number of moves in the game

called_cd_card = False #user can take only a single card at a time 

show_highscore = False

bg = pygame.image.load('bg/bg.jpg').convert()
bg = pygame.transform.scale(bg,screen_size)

closed_deck = pygame.image.load('Cards/covers/Yellow_back.jpg')
closed_deck = pygame.transform.scale(closed_deck,card_scale)

highscore_image = pygame.image.load('highscore.jpg')
#highscore_image = pygame.transform.scale(highscore_image,(500,330))

while in_game:
	
	# checking if comp_wins1
	# comp_win1()

	# helper function to display cards on screen
	def display_msg(x,X,Y,f = False,color = (255,255,255)):
			def text_objects(x,font):
				textSurface = font.render(x, True , color)
				return textSurface, textSurface.get_rect()
			if f:
				text = pygame.font.Font('freesansbold.ttf',25)
			else:
				text = pygame.font.SysFont('Candara',25)
			textSurf, textRect = text_objects(x, text)
			textRect.center = (X,Y)
			screen.blit(textSurf, textRect)

	pos=pygame.mouse.get_pos()

	# Loading screen		
	if loading_screen:
		screen.blit(bg_start,(0,0))
		pygame.display.flip()
		for event in pygame.event.get():
			if (event.type == KEYDOWN) and (event.key != K_ESCAPE):
				start_sound.play()
				display_msg('Shuffling Cards...',675,660,True,(255,255,0))
				pygame.display.update()
				time.sleep(5)
				loading_screen = False
			if ((event.type == KEYDOWN) and (event.key == K_ESCAPE)) or (event.type == pygame.QUIT):
				in_game = False
				sys.exit()
		continue

	for event in pygame.event.get(): # any inputs pygame recognises

		#reset game
		if (event.type == KEYDOWN) and (event.key == K_r):
			print()
			print('-------------------')
			print('THE GAME WAS RESET')
			print('-------------------')
			print()
			u.choose_cards()
			comp_cards = shuffle_for_comp()
			cards_drawn = ['14H']
			break


		if (event.type ==  pygame.QUIT) or ((event.type == KEYDOWN) and (event.key == K_ESCAPE)):  
			in_game = False
			sys.exit()

		if (pos[0] in range(882,1155)) and (pos[1] in range(5,70)):	
			if event.type == MOUSEBUTTONDOWN: 
				click_sound.play()
				show_highscore = not (show_highscore)
				break

		#Testing purposes
		if (event.type == KEYDOWN) and (event.key == K_RETURN):
			move_count+=1

		if event.type == MOUSEBUTTONDOWN:
			#selecting closed_deck_card
			if (pos[0] in range(250+150,250+150+card_scale[0])) and (pos[1] in range(200,200+card_scale[1])):
				select_cd_card = not (select_cd_card)
				click_sound.play()
				
			#cursor value, if True it returns the card number 
			cursor_value=u.check_cursor(pos)

		if (event.type == MOUSEBUTTONDOWN) and cursor_value[0]:
			# for selection of cards
			u.Card_chosen(cursor_value[1])
			click_sound.play()

		if (event.type == MOUSEBUTTONDOWN) and (pos[0] in range(250,250+card_scale[0])) and (pos[1] in range(200,200+card_scale[1])):
			#card from closed deck
			if called_cd_card: #to avoid multiple card calls
				move_count+=1 #increment a move
			else:
				cards_drawn=closed_deck_card(u.cards)
				call_closed_card_count = True
				called_cd_card = True
				click_sound.play()

		if (event.type == MOUSEBUTTONDOWN) and ((pos[0] in range(1155,1500)) and (pos[1] in range(5,70))):
			#submission
			submit = True
			submit_sound.play()

		if (event.type == MOUSEBUTTONDOWN) and ((pos[0] in range(50,50+card_scale[0])) and (pos[1] in range(200,200+card_scale[1]))):
			# wildcard click
			nope_sound.play()

	
	# BACKGROUND
	screen.blit(bg,(0,0))

	if show_highscore:
		pygame.draw.rect(screen, (255, 255, 255), (0, 85 , screen_size[0], screen_size[1]-85))
		screen.blit(highscore_image,(450,200))
		pygame.display.update()
		continue
	
	#placing cd_card display first as swapping is done and then the user has to wait for the computer
	#first update the data, and then look for swap 
	if call_closed_card_count:	
		if select_cd_card:
			#wether to swap or not 
			if not (u.swap_cd()):
				#drawing blip over the card to indicate detection 
				pygame.draw.circle(screen,(69,255,255),(240+150,190),6)
		closed_deck_patta = pygame.image.load('Cards/patte/'+cards_drawn[-1]+'.jpg')	
		closed_deck_patta = pygame.transform.scale(closed_deck_patta,card_scale)
		screen.blit(closed_deck_patta,(250+150,200))
	
	#overlay
	#selected cards are shown here too 
	u.display_cards(screen)
	
	u.swap() #check if two cards are to be swapped

	#joker 2
	display_joker(u.joker2)

	#closed deck
	screen.blit(closed_deck,(250,200))
	pygame.draw.rect(screen, (0, 100, 255), (240, 190, card_scale[0]+20, card_scale[1]+20), 3)

	#closed deck card
	pygame.draw.rect(screen, (69, 255, 255), (240+150, 190, card_scale[0]+20, card_scale[1]+20), 3)

	# your number of moves and highscore
	moves_x_display = u.cardsPos[-2][0][0]+72
	display_msg('Move count: '+str(int(move_count/2)),moves_x_display,485)
	
	#highscore
	if (pos[0] in range(882,1155)) and pos[1] in range(5,70):
		#highlight highscore button
		pygame.draw.rect(screen, (255,255,0), (882, 0, 273,70), 3)

	#submit button
	if (pos[0] in range(1155,1500)) and (pos[1] in range(5,70)):
		#highlight submit button
		pygame.draw.rect(screen, (255, 255, 0), (1155, 0, 345, 70), 3)

	#check cards if submit 	
	if submit:
		#all cards set to false
		u.dict_cards()
		in_game = False
		break

	pygame.display.flip()

	#if computer has won
	if comp_win_var:
		lose_1()

	if not(bool(move_count%2)): #even moves are your moves

		pygame.mouse.set_visible(True)

	else: #computer move

		def display_msg(x,X,Y):
			def text_objects(x,font):
				textSurface = font.render(x, True , (255,255,255))
				return textSurface, textSurface.get_rect()
			text = pygame.font.SysFont('Calibri',18)
			textSurf, textRect = text_objects(x, text)
			textRect.center = (X,Y)
			screen.blit(textSurf, textRect)

		display_msg('CPU is playing...',250+200,171)
		pygame.display.update()
		pygame.mouse.set_visible(False)
		clock_sound.play()
		time.sleep(3.5)
		ping_sound.play()
		#cards_drawn = comp_move1(cards_drawn,u)
		(cards_drawn,comp_cards) = comp_move(comp_cards,cards_drawn)
		move_count+=1
		called_cd_card = False
		
colorama.init()
def cprint_r(string):
	print(colored(string, 'red'))
def cprint_g(string):
	print(colored(string, 'green'))
def cprint_b(string):
	print(colored(string, 'blue'))

#f in the chat (when lost)
def f():
	print()
	print(colored('  FFFFFFF', 'magenta'))
	print(colored('  FF', 'magenta'))
	print(colored('  FFFFF', 'magenta'))
	print(colored('  FF', 'magenta'))
	print(colored('  FF', 'magenta'))
	print(colored('  FF', 'magenta'))
	print()

def thankyou():
	#won
	
	#append score to file
	f = open('highscore.txt',"a")
	when = str(datetime.datetime.now())
	when = when[:when.rfind(':')]
	f.write(u.name +' '+ str(move_count)+' '+when+'\n')
	f.close()
	print()
	cprint_b('All sequences verified! ' + u.name + ' WINS!')
	print()
	print('THANK YOU FOR PLAYING')
	win_sound.play()
	time.sleep(10)
	sys.exit()

def lose():
	f()
	cprint_r('You Lost! :(')
	print('BYE!')
	lose_sound.play()
	time.sleep(5)
	sys.exit()

def display_num():
	
	def display_msg_card(x,X,Y,myfont=False):
		def text_objects(x,font):
			textSurface = font.render(x, True , (255,255,255))
			return textSurface, textSurface.get_rect()
		text = pygame.font.Font('freesansbold.ttf',25)
		if myfont:
			text = pygame.font.SysFont('Calibri',25)
		textSurf, textRect = text_objects(x, text)
		textRect.center = (X,Y)
		screen.blit(textSurf, textRect)

	display_msg_card(u.name + "'s Submitted In-Hand Cards",730,50,True)
	for i in range(len(u.cardsPos)):
		display_msg_card(str(i+1),u.cardsPos[i][0][0]+50,u.cardsPos[i][0][1]-26)

def convert_to_joker():
	print()
	print(colored('All wildcards are converted into jokers.','cyan'))
	for i in range(len(u.cards)):
		if int(u.cards[i][:-1]) == int(u.joker2[:-1]):
			u.cards[i] = '14S' #replacing those cards with jokers

def eval_input():

	#initializing the lists
	l1=[] #first pure sequence
	l2=[] #second pure/impure sequence
	l3=[] #third sequence/set
	l4=[] #fourth sequence/set

	#graphics heavy, shifting to command prompt
	print()
	sprint('# Input your valid sequences/runs to declare ')
	sprint('# Enter the sequence in required order ')
	print()
	sprint('1. Input first sequence [PURE] :')
	print('-> ',end='')
	l1 = list(map(int,input().split()))
	sprint('2. Input second sequence [PURE/IMPURE] :')
	print('-> ',end='')
	l2 = list(map(int,input().split()))
	sprint('3. Input third sequence/set : ')
	l3_choice = input('Sequence or set: ')
	print('-> ',end='')
	l3 = list(map(int,input().split()))
	sprint('4. Input fourth sequence/set :')
	l4_choice = input('Sequence or set: ')
	print('-> ',end='')
	l4 = list(map(int,input().split()))
	print()

	l3_choice = l3_choice.lower()
	l4_choice = l4_choice.lower()

	#converting to boolean
	#True for seq, False for set
	if l3_choice == 'sequence':
		l3_choice = True 
	elif l3_choice == 'set':
		l3_choice = False
	else:
		raise RuntimeError('Wrong Input')
	
	if l4_choice == 'sequence':
		l4_choice = True 
	elif l4_choice == 'set':
		l4_choice = False
	else:
		raise RuntimeError('Wrong Input')

	return (l1,l2,l3,l4,l3_choice,l4_choice)

def evaluate(l1,l2,l3,l4,l3_choice,l4_choice):

	global auto
	def reduceBy1(l): # as for user, 0 card is 1st card 
		for i in range(len(l)):
			l[i]-=1

	reduceBy1(l1)
	reduceBy1(l2)
	reduceBy1(l3)
	reduceBy1(l4)

	def cards_num_check(l1,l2,l3,l4):
		l=[]
		l.append(l1)
		l.append(l2)
		l.append(l3)
		l.append(l4)
		a=sorted(l,key = lambda x:len(x))
		if (len(a[0]) == 3) and (len(a[1]) == 3) and (len(a[2]) == 3) and (len(a[3]) == 4):
			return True
		else:
			return False

	def check1(l):
		for i in l:
			if l.count(i)>1:
				return False
		return True

	def check2(l):
		checklist=[]
		suit=[]
		for i in l:
			if u.cards[i][:-1] == '14': #joker detected
				return False
			else:
				checklist.append(int(u.cards[i][:-1]))
				suit.append(u.cards[i][-1])
		
		#all suits should be the same
		if suit.count(suit[0])!=len(l):
			return False
		
		checklist=sorted(checklist)
		check = True
		for i in range(len(checklist)-1):
			if checklist[i+1]-checklist[i]==1:
				check = check and True
			else:
				check = check and False
		return check

	def check3(l):
		checklist=[]
		suit=[]
		for i in l:
			checklist.append(int(u.cards[i][:-1]))
			suit.append(u.cards[i][-1])
		if checklist.count(14)>=2:
			return False
		if not((suit.count(suit[0]) == len(l)) or (suit.count(suit[0]) == len(l)-1) or (suit.count(suit[1]) == len(l)) or (suit.count(suit[1]) == len(l)-1)):
			return False
		check = True
		checklist = sorted(checklist)
		for i in range(len(checklist)-2):
			if checklist[i+1]-checklist[i]==1:
				check = check and True
			elif checklist[i+1]-checklist[i]==2:
				if checklist[-1] == 14:
					check = check and True
				else:
					check = check and False
			else:
				check = check and False
		return check

	def check4(l,sequence):
		if sequence:
			return check3(l)
		else:
			def set_check(cards):
				check = True
				key = cards[0][:-1]
				for i in cards:
					if i[:-1] == key:
						check = check and True
					else:
						check = check and False
				return check
			#check for set 
			cards=[]
			joker_count = 0 
			for i in l:
				if u.cards[i][:-1] == '14':
					joker_count+=1
				cards.append(u.cards[i])
			if joker_count>1:
				return False
			cards = sorted(cards,key = lambda x:int(x[:-1]))
			if int(cards[-1][:-1]) == 14: #joker is present 
				cards = cards[:-1]
			return set_check(cards)

	#game logic here
	#submission logic
	l=l1+l2+l3+l4
	if not(sorted(l) == [0,1,2,3,4,5,6,7,8,9,10,11,12]):
		if not auto:
			pygame.mixer.music.stop()
			troll_sound.play()
			time.sleep(2)
			cprint_r('All cards not mentioned, you lose.'.upper())
		return False
	if not(cards_num_check(l1,l2,l3,l4)):
		if not auto:
			pygame.mixer.music.stop()
			troll_sound.play()
			time.sleep(2)
			cprint_r('Cards are not set in orders of 4 & 3'.upper())
		return False
	if not(check1(l)):
		if not auto:
			pygame.mixer.music.stop()
			troll_sound.play()
			time.sleep(2)
			cprint_r('Cards repeated, you lose.'.upper())
		return False
	if not(check2(l1)):
		if not auto:
			cprint_r('Wrong sequence 1, you lose.'.upper())
		return False
	else:
		if not auto:
			cprint_g('Sequence 1 right!'.upper())
	if not(check3(l2)):
		if not auto:
			cprint_r('Wrong sequence 2, you lose.'.upper())
		return False
	else:
		if not auto:
			cprint_g('Sequence 2 right!'.upper())
	if not(check4(l3,l3_choice)):
		if not auto:
			cprint_r('Wrong sequence 3, you lose.'.upper())
		return False
	else:
		if not auto:
			cprint_g('Sequence 3 right!'.upper())
	if not(check4(l4,l4_choice)):
		if not auto:
			cprint_r('Wrong sequence 4, you lose.'.upper())
		return False
	else:
		if not auto:
			cprint_g('Sequence 4 right!'.upper())

	return True 

# after submission, all wildcards are to be converted to jokers
convert_to_joker()

# at this stage program only displays the cards of the user 
pygame.init()

# loading sounds
win_sound = pygame.mixer.Sound('sounds/win.wav')
troll_sound = pygame.mixer.Sound('sounds/troll.wav')

screen_size = (width,height) = (1500,360)
pygame.display.set_caption('Your Cards')
screen = pygame.display.set_mode(screen_size)
bg = pygame.image.load('bg/bg2.jpg').convert()
bg = pygame.transform.scale(bg,screen_size)
screen.blit(bg,(0,0))
u.display_cards(screen,150,submit)
display_num()
pygame.display.flip()
eval_ = False
toggle_caption = False

while True:
	if toggle_caption:
		pygame.display.set_caption('Your Cards')
		toggle_caption = not(toggle_caption)
	if not(toggle_caption):
		pygame.display.set_caption('Go to CMD!')
		toggle_caption = not(toggle_caption)
	for event in pygame.event.get(): # any inputs pygame recognises
		if ((event.type == KEYDOWN) and (event.key == K_ESCAPE)) or event.type ==  pygame.QUIT : 
			sys.exit()
		if (event.type == MOUSEBUTTONDOWN) or ((event.type == KEYDOWN) and (event.key == K_RETURN)):
			if not eval_:
				#auto evaluation
				print()
				sprint('Want your cards to be auto-evaluated? [Ordered Cards] : (y/n)' )
				auto = input().lower()
				print()

				pygame.mixer.music.stop()
				clock_sound.play()
				time.sleep(4)	

				if auto == 'y':
					auto = True
				else:
					auto = False
				
				if not(auto):
					(l1,l2,l3,l4,l3_choice,l4_choice) = eval_input()
					win = evaluate(l1,l2,l3,l4,l3_choice,l4_choice)
				
				if auto:
					l=[]
					for i in range(13):
						l.append(i+1)
					win = False
					for l3_choice in range(0,2):
						for l4_choice in range(0,2):
							win = win or evaluate(l[:5],l[5:8],l[8:11],l[11:],bool(l3_choice),bool(l4_choice)) 
							win = win or evaluate(l[:4],l[4:8],l[8:11],l[11:],bool(l3_choice),bool(l4_choice)) 
							win = win or evaluate(l[:4],l[4:7],l[7:11],l[11:],bool(l3_choice),bool(l4_choice)) 
							win = win or evaluate(l[:4],l[4:7],l[7:10],l[10:],bool(l3_choice),bool(l4_choice)) 
					if win:
						cprint_g('Sequence 1 right!'.upper())
						cprint_g('Sequence 2 right!'.upper())
						cprint_g('Sequence 3 right!'.upper())
						cprint_g('Sequence 4 right!'.upper())
					else:
						cprint_r("Cards don't pass the auto-evaluation!".upper())

				if win:
					thankyou()
				else:
					lose()
				eval_ = True

	time.sleep(0.40)
	pygame.display.flip()