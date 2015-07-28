#coding:utf-8
import pyaudio
import wave

class Record:
	def __init__(self, chunk=1024, wavFormat=pyaudio.paInt16, channels=1, rate=8000):
		self.chunk = chunk
		self.format = wavFormat
		self.channels = channels
		self.rate = rate
		self.pyaudio = pyaudio.PyAudio()

	def setChunk(self ,chunk):
		self.chunk = chunk

	def getChunk(self):
		return self.chunk

	def setFormat(self ,fmt):
		self.format = fmt

	def getFormat(self):
		return self.format

	def setChannels(self, channels):
		self.channels = channels

	def getChannels(self):
		return self.channels

	def setRate(self, rate):
		self.rate = rate

	def getRate(self):
		return self.rate

	def record(self, second):
		try:
			stream = self.pyaudio.open(format=self.format,
							channels=self.channels,
							rate=self.rate,
							input=True,
							frames_per_buffer=self.chunk)
		except:
			print u'ERROR: 创建音频流发生错误'
			return 
			
		print(u'开始录制:')
		recordFrames = []
		frameNum = int(self.rate * second / self.chunk)
		for i in range(frameNum):
			print u'......%.0f%%' % ((i + 1) * 100.0 / frameNum)
			data = stream.read(self.chunk)
			recordFrames.append(data)
		print(u'录制完成。')

		stream.stop_stream()
		stream.close()

		recordData = ''.join(recordFrames)

		return recordData

	def recordUntilNoSpeaking(self):
		pass

	def writeToWavFile(self, frames, name):
		try:	
			wf = wave.open(name, 'wb')
			wf.setnchannels(self.channels)
			wf.setsampwidth(self.pyaudio.get_sample_size(self.format))
			wf.setframerate(self.rate)
			wf.writeframes(frames)
			wf.close()
		except:
			print u'Error: 保存音频时时出错'

	def recordAndSave(self, name, second):
		frames = self.record(second)
		self.writeToWavFile(frames, name)
 
	def play(self, name):
		waveFrame = wave.open(name, 'rb')
		stream = self.pyaudio.open(format=self.pyaudio.get_format_from_width(waveFrame.getsampwidth()),
						channels=waveFrame.getnchannels(),
						rate=waveFrame.getframerate(),
						output=True)
  		data = waveFrame.readframes(self.chunk)
  
		while data != '':	
			stream.write(data)
			data = waveFrame.readframes(self.chunk)
  
		stream.stop_stream()	
		stream.close()

if __name__ == '__main__':
    rec = Record()
    rec.recordAndSave('test.wav', 2)

