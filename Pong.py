# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles

def read_value(file, variable_name): #extract values from the file
        l = file.readlines()
        for i in l:
                if i[0:3] == variable_name: #search for line
                        count = 0
                        for j in i[6:]:
                                count += 1
                                if j == " ":
                                        return int(i[6:count]) #return the integer
v = open("variables.txt")
WIDTH = read_value(v, "cwh")
HEIGHT = read_value(v, "cht")       
BALL_RADIUS = read_value(v, "brd")
PAD_WIDTH = read_value(v, "pwh")
PAD_HEIGHT = read_value(v, "pht")
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2,HEIGHT/2]
    ball_vel = [0,0]
    ball_vel[0] = read_value(v, "bhv")
    ball_vel[1] = read_value(v, "bvv")
    if direction == "Left":
        ball_vel[0] = - ball_vel[0]
    else:
        pass
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    ball_pos = [WIDTH/2,HEIGHT/2]
    paddle1_pos = HEIGHT/2
    paddle2_pos = HEIGHT/2
    paddle1_vel, paddle2_vel = 0, 0
    spawn_ball("Right")
    score1 = 0
    score2 = 0

def read_colour(file, object_name): #extract colour from file
        l = file.readlines()
        for i in l:
                if i[0:3] == object_name: #search for line
                        count = 0
                        for j in i[6:]:
                                count += 1
                                if j == " ":
                                        return (i[6:count]) #return the colour
                                
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, read_colour(v,"mcl"))
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, read_colour(v,"gcl"))
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, read_colour(v,"gcl"))
        
    # update ball
    
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    elif ball_pos[1] >= (HEIGHT-1)-BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS and ball_pos[1] <= HALF_PAD_HEIGHT+paddle1_pos and ball_pos[1] >=paddle1_pos - HALF_PAD_HEIGHT:
        ball_vel[0] = -1.1 * ball_vel[0]
    elif ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        spawn_ball("Right")
        score2 += 1
    elif ball_pos[0] >= (WIDTH-1)-BALL_RADIUS-PAD_WIDTH and ball_pos[1] <= HALF_PAD_HEIGHT+paddle2_pos and ball_pos[1] >=paddle2_pos - HALF_PAD_HEIGHT:
        ball_vel[0] = - 1.1 * ball_vel[0]
    elif ball_pos[0] >= (WIDTH-1)-BALL_RADIUS-PAD_WIDTH:
        spawn_ball("Left")
        score1 += 1
    
    # draw ball
    canvas.draw_circle(ball_pos,BALL_RADIUS,1,"White",read_colour(v,"bcl"))
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    canvas.draw_text("Player 1", (125, 50), 30, read_colour(v,"scl"))
    canvas.draw_text("Player 2", [400, 50], 30, read_colour(v,"scl"))
    canvas.draw_text(str(score1), (250, 50), 30, read_colour(v,"scl"))
    canvas.draw_text(str(score2), [350, 50], 30, read_colour(v,"scl"))
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos+paddle1_vel>= 40 and paddle1_pos+paddle1_vel <=360:
        paddle1_pos += paddle1_vel
    if paddle2_pos+paddle2_vel> 40 and paddle2_pos+paddle2_vel <=360:
        paddle2_pos += paddle2_vel
    # draw paddles   
    canvas.draw_line([PAD_WIDTH/2, HALF_PAD_HEIGHT+paddle1_pos],[PAD_WIDTH/2, paddle1_pos - HALF_PAD_HEIGHT], PAD_WIDTH, read_colour(v,"pcl"))
    canvas.draw_line([WIDTH - 1 - PAD_WIDTH/2, HALF_PAD_HEIGHT+paddle2_pos],[WIDTH - 1 - PAD_WIDTH/2, paddle2_pos - HALF_PAD_HEIGHT], PAD_WIDTH, read_colour(v,"pcl"))
    # draw scores
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -read_value(v, "pve")
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = read_value(v, "pve")
    current_key = chr(key)
    if current_key == "W":
        paddle1_vel = -read_value(v, "pve")
    elif current_key == "S":
        paddle1_vel = read_value(v, "pve")
        
    
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    current_key = chr(key)
    if current_key == "W":
        paddle1_vel = 0
    elif current_key == "S":
        paddle1_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Reset", new_game)

# start frame
new_game()
frame.start()
