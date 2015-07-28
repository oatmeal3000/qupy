#
# Makefile for simple rover
# A demo program for the Gertbot
# Motors are switched on or off using the Keypad and Numlock
# This makefile is for on the Raspberry-Pi

simple_rover: simple_rover.c gb_drivers.c gertbot_pi_uart.c gb_drivers.h gertbot_defines.h
	gcc -o simple_rover simple_rover.c gb_drivers.c gertbot_pi_uart.c

