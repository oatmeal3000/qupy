#coding:utf-8

from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
# --------------------------------------------------------------------------------
# demo主页: /demo
# --------------------------------------------------------------------------------
def home(request):
	return render(request, 'home.html') 



#------------------------------------------------------------------------------
# GPIO Page  :  /demo/gpio
#------------------------------------------------------------------------------

def gpioControl(request): 
    if gpioControl.gpio is None:  
        import common.gpio as gpioPin 
        gpioControl.gpio = gpioPin.getAllPins()  
    if request.method == 'GET': 
        pinSet = [['3.3V DC Power','DC Power 5V'],\
                  ['GPIO02 (SDA1,I2C)','DC Power 5V'], \
                  ['GPIO03 (SCL1,I2C)','Ground'], \
                  ['GPIO04 (GPIO_GCLK)','(TXD0) GPIO14'], \
                  ['Ground','(RXD0) GPIO15'], \
                  ['GPIO17 (GPIO_GEN0)','(GPIO_GEN1) GPIO18'], \
                  ['GPIO27 (GPIO_GEN2)','Ground'], \
                  ['GPIO22 (GPIO_GEN3)','(GPIO_GEN4) GPIO23'], \
                  ['3.3V DC Power','(GPIO_GEN5) GPIO24'], \
                  ['GPIO10 (SPI_MOSI)','Ground'], \
                  ['GPIO09 (SPI_MISO)','(GPIO_GEN6) GPIO25'], \
                  ['GPIO11 (SPI_CLK)','(SPI_CE0_N) GPIO08'], \
                  ['Ground','(SPI_CE1_N) GPIO07'], \
                  ['ID_SD (I2C ID EEPROM)','(I2C ID EEPROM) ID_SC'], \
                  ['GPIO05','Ground'], \
                  ['GPIO06','GPIO12'], \
                  ['GPIO13','Ground'], \
                  ['GPIO19','GPIO16'], \
                  ['GPIO26','GPIO20'], \
                  ['Ground','GPIO21']]

        tableStrings = ''
        for row in pinSet:
            tableStrings += '<tr><td align="right">'    
            if 'GPIO' in row[0]:
                    tableStrings += '<button type="button" class="btn w-xs btn-link "  onclick="reverseDirection(' 
                    pinIndex = int(row[0][4:6])
                    tableStrings += str(pinIndex) 
                    tableStrings += ')"><span id="direction'
                    tableStrings += str(pinIndex)
                    tableStrings += '">'
                    tableStrings += gpioControl.gpio[pinIndex].getFunctionStr()
                    tableStrings += '</span><span id="voltage'
                    tableStrings += str(pinIndex)
                    tableStrings += '">('
                    tableStrings += str(gpioControl.gpio[pinIndex].input())
                    tableStrings += ')</span></button>'
            tableStrings += '</td>'
            tableStrings += '<td><button type="button" class="btn w-xs '
            if 'DC' in row[0]:
                tableStrings += 'btn-danger2 '
            elif 'Ground' in row[0]:
                tableStrings += 'btn-primary '
            elif 'SPI' in row[0]:
                tableStrings += 'btn-danger '
            elif 'EEPROM' in row[0] or 'TXD' in row[0] or 'RXD' in row[0]:
                tableStrings += 'btn-warning '
            elif 'SDA' in row[0] or 'SCL' in row[0]:
                tableStrings += 'btn-info '
            else:
                tableStrings += 'btn-success '
            tableStrings += ' btn-block"'
            
            if 'GPIO' in row[0]:
                tableStrings += 'onclick="toggleValue('
                tableStrings += str(pinIndex)
                tableStrings += ')">'
            else:
                tableStrings += '>'
            
            tableStrings += row[0]
            tableStrings += '</button></td>'
            tableStrings += '<td><button type="button" class="btn w-xs '
            if 'DC' in row[1]:
                tableStrings += 'btn-danger2 '
            elif 'Ground' in row[1]:
                tableStrings += 'btn-primary '
            elif 'SPI' in row[1]:
                tableStrings += 'btn-danger '
            elif 'EEPROM' in row[1] or 'TXD' in row[1] or 'RXD' in row[1]:
                tableStrings += 'btn-warning '
            elif 'SDA' in row[1] or 'SCL' in row[1]:
                tableStrings += 'btn-info'
            else:
                tableStrings += 'btn-success '
            tableStrings += 'btn-block" '
            if 'GPIO' in row[1]:
                pinIndex = int(row[1][-2:]) 
                tableStrings += 'onclick="toggleValue('
                tableStrings += str(pinIndex)
                tableStrings += ')">'
            else:
                tableStrings += '>'
            tableStrings += row[1] 

            tableStrings += '</button></td>'
            tableStrings += '<td>'
            if 'GPIO' in row[1]:
                    tableStrings += '<button type="button" class="btn w-xs btn-link "  onclick="reverseDirection(' 
                    pinIndex = int(row[1][-2:])
                    tableStrings += str(pinIndex) 
                    tableStrings += ')"><span id="direction'
                    tableStrings += str(pinIndex)
                    tableStrings += '">'
                    tableStrings += gpioControl.gpio[pinIndex].getFunctionStr()
                    tableStrings += '</span><span id="voltage'
                    tableStrings += str(pinIndex)
                    tableStrings += '">('
                    tableStrings += str(gpioControl.gpio[pinIndex].input())
                    tableStrings += ')</span></button>'
 
            tableStrings += '</td>'
            tableStrings += '</tr>'

        return render(request, 'gpio.html', {'pinMatrix': tableStrings })
    elif  request.method == 'POST': 
        numPin = int(request.POST.get('num')) 
        commandTag = request.POST.get('command') 
        answer = {'result': None} 
        if  commandTag == 'direction': 
            func = gpioControl.gpio[numPin].reverse()
            answer['result'] = func 
        elif commandTag == 'value': 
            outputVoltage = gpioControl.gpio[numPin].toggle() 
            answer['result'] = outputVoltage  
        elif commandTag == 'input': 
            inputValues = {}
            for pin in gpioControl.gpio[1:]:
                if pin.getFunctionStr() == 'IN':
                    inputValues[pin.num] = str(pin.input())
            answer['result'] = inputValues 
        return JsonResponse(answer)
gpioControl.gpio = None


# --------------------------------------------------------------------------------
# 温度检测: /demo/temp
# --------------------------------------------------------------------------------
def tempSensing(request):
	if tempSensing.reader is None:
		tempSensing.reader = open('/sys/class/thermal/thermal_zone0/temp')
	reader = tempSensing.reader
	reader.seek(0)
	temp = float(reader.read()[:-1]) / 1000
	temp = round(temp, 1)

	query = request.GET.get('update', None)
	if query:
		return HttpResponse(temp)

	return render(request, 'temp.html', {'temp': temp}) 
tempSensing.reader = None

# --------------------------------------------------------------------------------
# 摄像头: /demo/camera
# --------------------------------------------------------------------------------
import cv2
def jpegStreamer(cap):
	while cap.isOpened():
		ret, frame = cap.read()
		if ret:
			ret, data = cv2.imencode('.jpg', frame)
		data = data.tostring()
		res  = '--liushuo\r\n'
		res += 'Content-Type: image/jpeg\r\n'
		res += 'Content-Length: %s\r\n\r\n' % len(data)
		res += data
		yield res
		#time.sleep(0.05)

def cameraDemo(request):
	if cameraDemo.cap is None:
		cameraDemo.cap = cv2.VideoCapture(0)
		cameraDemo.cap.set(3, 320.0)
		cameraDemo.cap.set(4, 240.0)

	if not request.GET.get('action', None):
		return render(request, 'stream.html')

	response = StreamingHttpResponse(jpegStreamer(cameraDemo.cap), 
					content_type='multipart/x-mixed-replace; boundary=liushuo')
	return response
cameraDemo.cap = None

# --------------------------------------------------------------------------------
# 小车控制: /demo/drive_car 
# --------------------------------------------------------------------------------

@csrf_exempt
def driveCar(request):
        if request.method == 'GET': 
                if not driveCar.driver:
                	from common.car_driver import CarDriver    
              		driveCar.driver = CarDriver()
		return render(request, 'drive_car.html')
	if request.method == 'POST':
		cmd = request.POST['command']
				
		driver = driveCar.driver
		if cmd == 'up':
			driver.goForward()
		elif cmd == 'down':
			driver.goBack()
		elif cmd == 'left':
			driver.turnLeft()
		elif cmd == 'right':
			driver.turnRight()
		elif cmd == 'stop':
			driver.stop()
		elif cmd == 'gear+':
			driver.gearUp()
		elif cmd == 'gear-':
			driver.gearDown()

                answer = {'speed': driver.gear} 
		return JsonResponse(answer)
driveCar.driver = None

# --------------------------------------------------------------------------------
# 声音识别: /demo/audio
# --------------------------------------------------------------------------------

from common.audio.recognition import recognition
from common.audio.pcm_converter import convert

@csrf_exempt
def audioDemo(request):
	if request.method == 'GET':
		response = render(request, 'audio_recognition.html')
	elif request.method == 'POST':
		try:
			pcmData = request.body
			res = recognition(pcmData)
			response = HttpResponse(res[0] if res else '')
		except Exception as e:
			print e
			raise

	return response 

# --------------------------------------------------------------------------------
# 声波测距: /demo/sound_ranging
# --------------------------------------------------------------------------------

def soundRanging(request):
	if soundRanging.sd is None:
		from common.soundranging import SoundRanging
		soundRanging.sd = SoundRanging()

	update = request.GET.get('update', None)
	if update:
		distance = soundRanging.sd.getDistance()
		distance = round(distance, 1)
		return JsonResponse({"distance": str(distance)})

	return render(request, 'sound_ranging.html')
soundRanging.sd = None 

# --------------------------------------------------------------------------------
# 光线感应: /demo/light_sensing
# --------------------------------------------------------------------------------

def lightSensing(request):
	if lightSensing.sensor is None:
		from common.lightsensing import LightSensor
		lightSensing.sensor = LightSensor()

	update = request.GET.get('update', None)
	if update:
		light = lightSensing.sensor.sensing()
		res = {}
		if light:
			res['result'] = u'有光线'
		else:
			res['result'] = u'无光线'
		return JsonResponse(res)

	return render(request, 'light_sensing.html')
lightSensing.sensor = None

# --------------------------------------------------------------------------------
# 声音感应: /demo/sound_sensing
# --------------------------------------------------------------------------------

def soundSensing(request):
	if soundSensing.sensor is None:
		from common.soundsensing import SoundSensor
		soundSensing.sensor = SoundSensor()

	update = request.GET.get('update', None)
	if update:
		sound = soundSensing.sensor.sensing()
		res = {}
		if sound:
			res['result'] = u'有声响'
		else:
			res['result'] = u'无声响'
		return JsonResponse(res)

	return render(request, 'sound_sensing.html')
soundSensing.sensor = None
