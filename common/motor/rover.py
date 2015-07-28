#
# Python Rover (PRover)
#
# the Gertbot drivers
import gertbot as gb

# Using curses to repond to single keyboard keys
import curses 

# This is for the development environment:
#BOARD = 1           # Which board we talk to 
#LEFT  = 0           # channel for left track
#RIGHT = 2           # channel for right track

BOARD = 0           # Which board we talk to 
LEFT  = 2           # channel for left track
RIGHT = 3           # channel for right track

# Forards and backwards are the same for left and right
# The trick is to reverse the motor connections for one  :-) 
RAMP  = gb.RAMP_050 # ramp speed=0.5 seconds
FORWD = gb.MOVE_A
BACKW = gb.MOVE_B
STOP  = gb.MOVE_STOP

# 
# gb.move_brushed(board,channel,direction)
#                 ^^^^^ ^^^^^^^ ^^^^^^^^^ 
#                 ||||| ||||||| ||||||||| 
#                 ||||| ||||||| ||||||||| 
#                 ||||| ||||||| +++++++++--------< Left, right, stop
#                 ||||| +++++++------------------< Which motor on board 0,1,2,3
#                 +++++--------------------------< which board 0,1,2,3


# Main program

# Get the curses screen
screen = curses.initscr()
  
# Open serial port to talk to Gertbot 
gb.open_uart(0)

# Setup the channels for brushed motors
gb.set_mode(BOARD,LEFT,gb.MODE_BRUSH)
gb.set_mode(BOARD,RIGHT,gb.MODE_BRUSH)
# set a ramp-up speed in case motors are big
gb.set_brush_ramps(BOARD,LEFT, RAMP,RAMP,0);
gb.set_brush_ramps(BOARD,RIGHT,RAMP,RAMP,0);
    
# Tell user what to expect
# in curses print does not work anymore. use addstr
screen.addstr("Gertbot example program for Python\n")
screen.addstr("Use numeric keypad keys control\n")
screen.addstr("Left  Both  Right\n")
screen.addstr("     Forward     \n")
screen.addstr("  7     8     9  \n")
screen.addstr("                 \n")
screen.addstr("  4    Stop   6  \n")
screen.addstr("                 \n")
screen.addstr("  1     2     3  \n")
screen.addstr("     Reverse     \n")
screen.addstr("Left  Both  Right\n")
screen.addstr("Don't forget to set numlock on!!!!\n")
screen.addstr("Use Q or q to quit\n")
screen.addstr("\n")


run = 1
while run==1 :
  key = screen.getch() # Key?
  if key==ord('q') :
    run = 0 # stop running
    
  if key==ord('1') : 
     gb.pwm_brushed(BOARD, LEFT, 50, 40)
     gb.move_brushed(BOARD,LEFT,BACKW) # Left backwards 
     #gb.pwm_brushed(BOARD, LEFT, 10, 0) 

  if key==ord('2') : 
     gb.move_brushed(BOARD,LEFT,BACKW)  # Left backwards 
     gb.move_brushed(BOARD,RIGHT,BACKW) # Right backwards 

  if key==ord('3') : 
     gb.move_brushed(BOARD,RIGHT,BACKW) # Right backwards 

  if key==ord('4') :
     gb.move_brushed(BOARD,LEFT,STOP) # Left stop 

  if key==ord('5') : 
     gb.move_brushed(BOARD,LEFT,STOP)  # Left stop 
     gb.move_brushed(BOARD,RIGHT,STOP) # Right stop 

  if key==ord('6') :
     gb.move_brushed(BOARD,RIGHT,STOP) # Right stop 

  if key==ord('7') :
     gb.move_brushed(BOARD,LEFT,FORWD) # Left forwards 

  if key==ord('8') :
     gb.move_brushed(BOARD,LEFT,FORWD)  # Left forwards 
     gb.move_brushed(BOARD,RIGHT,FORWD) # Right forwards 

  if key==ord('9') :
     gb.move_brushed(BOARD,RIGHT,FORWD) # Right forwards 

# on exit stop everything
gb.emergency_stop()
# Set terminal behaviour normal again
curses.endwin()

