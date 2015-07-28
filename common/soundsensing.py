#coding:utf8
import RPi.GPIO as GPIO

class SoundSensor:
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
		return not GPIO.input(self.doPin)

if __name__ == '__main__':
	import time
	sensor = SoundSensor()
	while True:
		data = sensor.sensing()
		if data:
			print u'检测到声音'
		else:
			print u'未检测到声音'
