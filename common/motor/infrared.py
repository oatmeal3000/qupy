#coding:utf8
import RPi.GPIO as GPIO
from time import time

INVALID = -1
COMMAND = 1
REPEAT  = 2

START_LOW_DURATION				= 0.009
START_COMMAND_HIGH_DURATION 	= 0.0045
START_REPEAT_HIGH_DURATION		= 0.00225

class InfraredReciever:
	DEFAULT_RECV_GPIO_PIN 	= 20
	# COMMAND:
	#__     9ms	     	   _________    
	#  |__________________|   4.5   |____

	# REPEAT :
	#__     9ms	           _____
	#  |__________________| 2.25|____

	def __init__(self, pin=DEFAULT_RECV_GPIO_PIN):
		self.initGPIO(pin)

	def initGPIO(self, pin):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pin, GPIO.IN, GPIO.PUD_DOWN)
		self.recvPin = pin

	def cleanupGPIO(self):
		GPIO.cleanup()

	def waitForStart(self):
		while True:
			# wait for low
			while GPIO.input(self.recvPin): pass
			ts = time()
			# wait for high
			while not GPIO.input(self.recvPin): pass
			te = time()
			lowdt = te - ts
			if abs(lowdt - START_LOW_DURATION) > 0.0002:
				continue
			ts = te
			# wait for low
			while GPIO.input(self.recvPin): pass
			te = time()
			highdt = te - ts
			if abs(highdt - START_COMMAND_HIGH_DURATION) < 0.0002:
				return COMMAND
			if abs(highdt - START_REPEAT_HIGH_DURATION) < 0.0002:
				return REPEAT

	def recvAddrAndCmd(self):
		res = [0] * 32
		for i in xrange(32):
			while not GPIO.input(self.recvPin): pass
			ts = time()
			while GPIO.input(self.recvPin): pass
			te = time()
			res[i] = te - ts
		# last brust
		while not GPIO.input(self.recvPin): pass
		return res

	def checkValid(self, data):
		return data[2] ^ 0xff ==  data[3]

	def decode(self, data):
		# s to ms
		data = [round(t * 1000, 2) for t in data]
		f = lambda a: int(''.join(['1' if t > 1.0 else '0' for t in a])[::-1], 2)
		#f = lambda a: ''.join(['1' if t > 1.0 else '0' for t in a])[::-1]
		return map(f, [data[i:i+8] for i in xrange(0, 32, 8)])

	def recv(self):
		start = self.waitForStart()
		data = None
		if start == COMMAND:
			data = self.recvAddrAndCmd()
			data = self.decode(data) 
			if not self.checkValid(data):
				return INVALID, None

		return start, data

if __name__ == '__main__':
	#test()
	reciver = InfraredReciever()
	while True:
		data = reciver.recv()
		print data
