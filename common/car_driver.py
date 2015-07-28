#from motor.motor import MotorControllor
from motor.l298n import MotorControllor

MAX_GEAR = 8
MOTOR_STATE_STOP 	= 0
MOTOR_STATE_RUNNING = 1

class CarDriver:
	def __init__(self):
		self.mc = MotorControllor.getInstance()
		self.gear = 0
		self.direction = 1
		self.motorsState = [MOTOR_STATE_STOP] * 2

	def stop(self):
		self.mc.stopFrontLeft()
		self.mc.stopFrontRight()
		self.gear = 0 

	def turnRight(self):
		self.mc.stopFrontRight()	
		self.mc.runFrontLeft(self.direction * self.gear)
	
	def turnLeft(self):
		self.mc.stopFrontLeft()
		self.mc.runFrontRight(self.direction * self.gear)

	def goForward(self):
		print 'go forward'
		self.direction = 1
		if self.gear == 0:
			self.gear = 1

		self.mc.runFrontLeft(self.direction * self.gear)
		self.mc.runFrontRight(self.direction * self.gear)

	def goBack(self):
		self.direction = -1
		if self.gear == 0:
			self.gear = 1
		
		self.mc.runFrontLeft(self.direction * self.gear)
		self.mc.runFrontRight(self.direction * self.gear)

	def gearUp(self):
		if self.gear < MAX_GEAR:
			self.gear += 1

		self.mc.runFrontLeft(self.direction * self.gear)
		self.mc.runFrontRight(self.direction * self.gear)

	def gearDown(self):
		if self.gear > 1:
			self.gear -= 1

		self.mc.runFrontLeft(self.direction * self.gear)
		self.mc.runFrontRight(self.direction * self.gear)
		
if __name__ == '__main__':
	a = CarDriver()
	a.goForward()
	from time import sleep
	sleep(2)
	a.gearUp()
	sleep(2)
	a.gearUp()
	sleep(2)
	a.gearUp()
	sleep(2)
		
	a.stop()
