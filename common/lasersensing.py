#coding:utf8
import RPi.GPIO as GPIO
from time import time

class LaserSensor:
	DEFAULT_DO_GPIO_PIN = 16

	def __init__(self, pin=DEFAULT_DO_GPIO_PIN):
		self.initGPIO(pin)
		self.doPin = pin

	def initGPIO(self, pin):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pin, GPIO.IN, GPIO.PUD_DOWN)

	def cleanupGPIO(self):
		GPIO.cleanup()

	def sensing(self):
		return GPIO.input(self.doPin)

if __name__ == '__main__':
	import time
	sensor = LaserSensor()
	while True:
		data = sensor.sensing()
		if data:
			print u'检测到激光'
		else:
			print u'未检测激光'
