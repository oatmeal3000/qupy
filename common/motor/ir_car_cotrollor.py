from infrared import InfraredReciever, INVALID, COMMAND, REPEAT
from motor import MotorControllor

UP_KEY_VALUE 		= 202
DOWN_KEY_VALUE 		= 210
LEFT_KEY_VALUE 		= 153
RIGHT_KEY_VALUE 	= 193
OK_KEY_VALUE		= 206

mc = MotorControllor.getInstance()
reciver = InfraredReciever()
while True:
	t, data = reciver.recv()
	if t != COMMAND:
		continue
	key = data[2]
	print key
	if key == UP_KEY_VALUE:
		mc.runFrontLeft(3)
		mc.runFrontRight(3)
	elif key == DOWN_KEY_VALUE:
		mc.runFrontRight(-3)
		mc.runFrontLeft(-3)
	elif key == LEFT_KEY_VALUE:
		mc.stopFrontLeft()
		mc.runFrontRight(1)
	elif key == RIGHT_KEY_VALUE:
		mc.stopFrontRight()
		mc.runFrontLeft(1)
	elif key == OK_KEY_VALUE:
		mc.stopFrontLeft()
		mc.stopFrontRight()

