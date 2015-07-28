#
# Python Rover (PRover)
#
# the Gertbot drivers
import gertbot as gb

BOARD = 0           	  # default board id
FRONT_LEFT  = 0           # channel for left track
FRONT_RIGHT = 1           # channel for right track
BACK_LEFT   = 2           # channel for left track
BACK_RIGHT  = 3           # channel for right track

# Forards and backwards are the same for left and right
# The trick is to reverse the motor connections for one  :-) 
RAMP  = gb.RAMP_050 # ramp speed=0.5 seconds
FORWD = gb.MOVE_A
BACKW = gb.MOVE_B
STOP  = gb.MOVE_STOP

DEFAULT_PWM_FREQ = 50 # 50hz

class MotorControllor:
	_instance = None
	@staticmethod
	def getInstance():
		if MotorControllor._instance is None:
			MotorControllor._instance = MotorControllor()
		return MotorControllor._instance	

	def __init__(self):
		gb.open_uart(0)
		# Setup the channels for brushed motors
		gb.set_mode(BOARD, FRONT_LEFT, gb.MODE_BRUSH)
		gb.set_mode(BOARD, FRONT_RIGHT, gb.MODE_BRUSH)
		gb.set_mode(BOARD, BACK_LEFT, gb.MODE_BRUSH)
		gb.set_mode(BOARD, BACK_RIGHT, gb.MODE_BRUSH)
		# set a ramp-up speed in case motors are big
		gb.set_brush_ramps(BOARD, FRONT_LEFT, RAMP,RAMP, 0)
		gb.set_brush_ramps(BOARD, FRONT_RIGHT,RAMP,RAMP, 0)
		gb.set_brush_ramps(BOARD, BACK_LEFT, RAMP,RAMP, 0)
		gb.set_brush_ramps(BOARD, BACK_RIGHT,RAMP,RAMP, 0)

	def runMotor(self, motorId, direction, speed=1, freq=DEFAULT_PWM_FREQ):
		gb.pwm_brushed(BOARD, motorId, freq, 70 + speed * 10)
		gb.move_brushed(BOARD, motorId, direction)

	def stopMotor(self, motorId):
		gb.move_brushed(BOARD, motorId, STOP)  # Left stop 

	def runFrontLeft(self, speed=1):
		direction = FORWD if speed > 0 else BACKW
		self.runMotor(FRONT_LEFT, direction, abs(speed))

	def runFrontRight(self, speed=1):
		direction = FORWD if speed > 0 else BACKW
		self.runMotor(FRONT_RIGHT, direction, abs(speed))

	def runBackLeft(self, speed=1):
		direction = FORWD if speed > 0 else BACKW
		self.runMotor(BACK_LEFT, direction, abs(speed))

	def runBackRight(self, speed=1):
		direction = FORWD if speed > 0 else BACKW
		self.runMotor(BACK_RIGHT, direction, abs(speed))

	def stopFrontLeft(self):
		self.stopMotor(FRONT_LEFT)

	def stopFrontRight(self):
		self.stopMotor(FRONT_RIGHT)

	def stopBackLeft(self):
		self.stopMotor(BACK_LEFT)

	def stopBackRight(self):
		self.stopMotor(BACK_RIGHT)

	def shutDownAll(self):
		gb.emergency_stop()

if __name__ == '__main__':
	import time
	mc = MotorControllor.getInstance()
	mc.runFrontRight(3)
	time.sleep(10)
	mc.stopFrontRight()
