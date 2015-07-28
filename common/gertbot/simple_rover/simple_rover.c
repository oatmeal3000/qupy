//
// Simple Rover (SRover)
// Control motors connected to a gertbot
// using the C-drivers
//

#include <stdio.h>
#include "gb_drivers.h"

#define BOARD 0  // Which board we talk to 
#define LEFT  0  // channel for left track
#define RIGHT 1  // channel for right track
#define RAMP  GB_RAMP_050 // ramp speed=0.5 secconds

int main(int argc, char *argv[])
{ int running,key,temp;
  
  // Open serial port to talk to Gertbot 
  if (!open_connection(0))
    return 1;
    
  // Setup the channels 0 and 1 on board 0 for brushed motors
  set_mode(BOARD,LEFT,GB_MODE_BRUSH);
  set_mode(BOARD,RIGHT,GB_MODE_BRUSH);
  // Set a ramp up/down time of 0.5 seconds, halt is immediate
  set_brush_ramps(BOARD,LEFT, GB_RAMP_050,GB_RAMP_050,GB_RAMP_NONE);
  set_brush_ramps(BOARD,RIGHT,GB_RAMP_050,GB_RAMP_050,GB_RAMP_NONE);
    
  printf("Gertbot example program\n");
  printf("This program is for two brushed motors\n");
  printf("It assumes the board number is set to %d\n",BOARD);
  printf("The motors are connected to outputs %d and %d\n",LEFT,RIGHT);
  printf("Use numeric keypad keys control\n");
  printf("Left  Both  Right\n");
  printf("     Forward     \n");
  printf("  7     8     9  \n");
  printf("                 \n");
  printf("  4    Stop   6  \n");
  printf("                 \n");
  printf("  1     2     3  \n");
  printf("     Reverse     \n");
  printf("Left  Both  Right\n");
  printf("Don't forget to set numlock on!!!!\n");
  printf("Use Q or q to quit\n");
  printf("\n");
  
  // Go into loop
  running = 1;
  while (running)
  {
    if (_kbhit())
    { 
      key = _getch();
      putchar(key);
      switch (key)
      {
      case 'q' : 
      case 'Q' : running = 0;
                 break;
      case '1' : move_brushed(BOARD,LEFT,GB_MOVE_B); // Left backwards 
                 break;
      case '2' : move_brushed(BOARD,LEFT,GB_MOVE_B); // Left backwards 
                 move_brushed(BOARD,RIGHT,GB_MOVE_B); // Right backwards 
                 break;
      case '3' : move_brushed(BOARD,RIGHT,GB_MOVE_B); // Right backwards 
                 break;
      case '4' : move_brushed(BOARD,LEFT,GB_MOVE_STOP); // Left stop 
                 break;
      case '5' : move_brushed(BOARD,LEFT,GB_MOVE_STOP); // Left stop 
                 move_brushed(BOARD,RIGHT,GB_MOVE_STOP); // Right stop 
                 break;
      case '6' : move_brushed(BOARD,RIGHT,GB_MOVE_STOP); // Right stop 
                 break;
      case '7' : move_brushed(BOARD,LEFT,GB_MOVE_A); // Left forwards 
                 break;
      case '8' : move_brushed(BOARD,LEFT,GB_MOVE_A); // Left forwards 
                 move_brushed(BOARD,RIGHT,GB_MOVE_A); // Right forwards 
                 break;
      case '9' : move_brushed(BOARD,RIGHT,GB_MOVE_A); //Right forwards 
                 break;
      } // switch 
    } // kbhit
  } // while running 
  
  // At exit send emergency stop
  // to remove power from all motors 
  emergency_stop();
#ifdef _WIN32
#else
  // restore terminal input to normal
  system("stty echo cooked");
#endif    
  
} // main 

#ifdef _WIN32
#else

// emulate windows kbhit and getch routines
// for linux 

int init = 0;
int c=0;
int _kbhit()
{ if (init==0)
  { system("stty raw -echo");
    init=1;
  }
  if (c)
    return 1;
  c = getchar();
  if (c==-1)
  { c = 0;
    return 0;
  }
  return 1;
} // _kbhit

int _getch()
{ int k;
  if (c)
  { k=c;
    c = 0;
    return k;
  }
  c = getchar();
  return c;
} // _getch

#endif 
