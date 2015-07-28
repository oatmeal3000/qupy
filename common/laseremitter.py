#coding:utf8
import RPi.GPIO as GPIO
from time import time

class LaserEmitter:
	DEFAULT_S_GPIO_PIN = 12

	def __init__(self, pin=DEFAULT_S_GPIO_PIN):
		self.initGPIO(pin)
		self.sPin = pin

	def initGPIO(self, pin):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

	def cleanupGPIO(self):
		GPIO.cleanup()

	def emit(self):
		GPIO.output(self.sPin, GPIO.HIGH)

	def unemit(self):
		GPIO.output(self.sPin, GPIO.LOW)


if __name__ == '__main__':
	import time
	le = LaserEmitter()
	while True:
		c = raw_input('input:')
		if c == 'j':
			le.emit()
		elif c == 'k':
			le.unemit()
