#
#  L298N Driver
# 
#  IN1 ---- GPIO23 
#  IN2 ---- GPIO24
#  ENA ---- GPIO18
#
#  IN3 ---- GPIO21
#  IN4 ---- GPIO20
#  ENB ---- GPIO16
#

import sys
sys.path.append("..")
from common.gpio import GPIOPin 
import RPi.GPIO as gpio

BOARD = 0           	  # default board id
FRONT_LEFT  = 0           # channel for left track
FRONT_RIGHT = 1           # channel for right track
BACK_LEFT   = 2           # channel for left track
BACK_RIGHT  = 3           # channel for right track

FORWD       = 1
BACKW       = -1

MAX_SPEED   = 8


DEFAULT_PWM_FREQ = 50 # 50hz

class MotorControllor:
	_instance = None
	@staticmethod
	def getInstance():
		if MotorControllor._instance is None:
			MotorControllor._instance = MotorControllor()
		return MotorControllor._instance	

	def __init__(self):
                self.in1 = GPIOPin(23)
                self.in1.setFunction(gpio.OUT, 0)
                self.in2 = GPIOPin(24)
                self.in2.setFunction(gpio.OUT, 0)
                self.enA = GPIOPin(18)
                self.enA.pwmInit(10)  # Frequency is set to 10
                self.enA.pwmStart(0)     # Initial duty cycle is 0
                self.in3 = GPIOPin(21)
                self.in3.setFunction(gpio.OUT, 0)
                self.in4 = GPIOPin(20)
                self.in4.setFunction(gpio.OUT, 0)
                self.enB = GPIOPin(16)
                self.enB.pwmInit(10)
                self.enB.pwmStart(0)
                self.speed = 0
                

	def runMotor(self, motorId, direction, speed=1, freq=DEFAULT_PWM_FREQ):
                if speed > MAX_SPEED:
                    speed = MAX_SPEED 
                self.speed = abs(speed)
                if motorId == FRONT_LEFT: 
                    self.enA.pwmChangeDutyCycle( speed * 10.0 )
                    if direction == FORWD:
                        self.in1.output(gpio.HIGH)    
                        self.in2.output(gpio.LOW)
                    else:
                        self.in1.output(gpio.LOW)
                        self.in2.output(gpio.HIGH)
                elif motorId == FRONT_RIGHT:
                    self.enB.pwmChangeDutyCycle( speed * 10.0 )
                    if direction == FORWD:
                        self.in3.output(gpio.HIGH)
                        self.in4.output(gpio.LOW)
                    else:
                        self.in3.output(gpio.LOW)
                        self.in4.output(gpio.HIGH)

	def stopMotor(self, motorId):
                if motorId == FRONT_LEFT:
                    self.in1.output(gpio.HIGH)
                    self.in2.output(gpio.HIGH)
                elif motorId == FRONT_RIGHT:
                    self.in3.output(gpio.HIGH)
                    self.in4.output(gpio.HIGH)

	def runFrontLeft(self, speed=1):
		direction = FORWD if speed > 0 else BACKW
		self.runMotor(FRONT_LEFT, direction, abs(speed))
                self.speed = abs(speed)

	def runFrontRight(self, speed=1):
		direction = FORWD if speed > 0 else BACKW
		self.runMotor(FRONT_RIGHT, direction, abs(speed))
                self.speed = abs(speed)

	def stopFrontLeft(self):
		self.stopMotor(FRONT_LEFT)

	def stopFrontRight(self):
		self.stopMotor(FRONT_RIGHT)

	def shutDownAll(self):
	        self.stopMotor(FRONT_LEFT)	
                self.stopMotor(FRONT_RIGHT)
                self.speed = 0

if __name__ == '__main__':
	import time
	mc = MotorControllor.getInstance()
        time.sleep(3)
	mc.runFrontRight(2)
	time.sleep(5)
	mc.stopFrontRight()
        time.sleep(3)
        mc.runFrontLeft(2)
        time.sleep(3)
        mc.stopFrontLeft()
        time.sleep(2)
        mc.runFrontRight(-2)
        time.sleep(2)
        mc.stopFrontRight()
