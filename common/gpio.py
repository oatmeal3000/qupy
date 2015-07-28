from RPi import GPIO as gpio

#mode init
gpio.setmode(gpio.BCM)

_gpioFuncDict = {
	gpio.OUT: 'OUT',
	gpio.IN: 'IN', 
	gpio.SERIAL: 'SERIAL',
	gpio.SPI: 'SPI',
	gpio.I2C: 'I2C',
	gpio.HARD_PWM:'HARD_PWM',
	gpio.UNKNOWN: 'UNKNOWN',
}

class GPIOPin:
	def __init__(self, num):
		self.num = num
		func = gpio.gpio_function(num)
		if func not in [gpio.SERIAL, gpio.SPI, gpio.I2C]:
			gpio.setup(num, func)

	def setFunction(self, func, ininValue=None):
		if ininValue:
			gpio.setup(self.num, func, ininValue)
		else:
			gpio.setup(self.num, func)

	def getFunction(self):
		return gpio.gpio_function(self.num)
	
	def getFunctionStr(self):
		func = self.getFunction()
		return _gpioFuncDict.get(func)

	def input(self):
                func = gpio.gpio_function(self.num)  
		if func not in [gpio.SERIAL, gpio.SPI, gpio.I2C]:
		    return gpio.input(self.num)
                else:
                    return 0

	def output(self, value):
		gpio.output(self.num, value)

	def toggle(self):
		func = self.getFunction() 
		if func == gpio.OUT:
			old = self.input()
			new = gpio.LOW if old == gpio.HIGH else gpio.HIGH
			self.output(new)
                        return str(new)
 
        def reverse(self):
                func = self.getFunction()
                if func == gpio.OUT:
		        self.setFunction(gpio.IN)
                        return 'IN'
                elif func == gpio.IN:
		        self.setFunction(gpio.OUT)
                        return 'OUT'

	# function PWM
	def pwmInit(self, frequency):
		self.setFunction(gpio.OUT)
		self.pwm = gpio.PWM(self.num, frequency)

	def pwmClean(self):
		self.pwmStop()
		gpio.cleanup()
		self.pwm = None

	def pwmStart(self, dc=50.0):
		self.pwm.start(dc)

	def pwmStop(self):
		self.pwm.stop()

	def pwmChangeFrequency(self, frequency):
		self.pwm.ChangeFrequency(frequency)

	def pwmChangeDutyCycle(self, dc):
		#dc: 0.0 ~ 100.0
		self.pwm.ChangeDutyCycle(dc)

GPIO_PINS_NUM = 27
_allPins = [None] + [GPIOPin(i) for i in range(1, GPIO_PINS_NUM + 1)]

# get gpio instance
def getGPIOPin(num):
	return _allPins[i]

def getAllPins():
        return _allPins

# test
if __name__ == '__main__':
	for i in range(1, GPIO_PINS_NUM):
		pin = getGPIOPin(i)
		print pin.getFunctionStr()
		if pin.getFunction() == gpio.IN:
			print pin.input()
	pin = getGPIOPin(16)
	pin.setFunction(gpio.OUT)
	pin.output(gpio.HIGH)
	print pin.input()
	pin.output(gpio.LOW)
	print pin.input()
	pin.toggle()
	print pin.input()
	pin.toggle()
	print pin.input()

	import time
	pin.pwmInit(5)
	pin.pwmStart(40.0)
	time.sleep(5)
	pin.pwmChangeFrequency(2)
	pin.pwmChangeDutyCycle(20.0)
	time.sleep(5)
	pin.pwmStop()
	pin.pwmClean()

