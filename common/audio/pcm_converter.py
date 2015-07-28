#coding:utf-8

import audiotools
def convert(wavData, sample_rate=8000, channels=1, bits_per_sample=16, channel_mask=0):
	with open('tmp.wav', 'w') as f:
		f.write(wavData)
		
	wa = audiotools.open('tmp.wav')
	pcmReader = wa.to_pcm()
	reader = audiotools.PCMConverter(pcmReader, sample_rate=sample_rate, channels=channels, \
				bits_per_sample=bits_per_sample, channel_mask=channel_mask)
	frames = [] 
	while True:
		data = reader.read()
		if not data: break
		frames.append(data.to_bytes(False, True))

	reader.close()
	pcmReader.close()

	return b''.join(frames)

# test
if __name__ == '__main__':
	w = audiotools.open('post_audio.wav')
	pcmReader = w.to_pcm()
	reader = audiotools.PCMConverter(pcmReader, sample_rate=8000, channels=1, \
				bits_per_sample=16, channel_mask=0)

	frames = [] 
	while True:
		data = reader.read()
		if not data: break
		frames.append(data.to_bytes(False, True))

	allData = ''.join(frames)

	from record import Record
	recorder = Record()
	recorder.writeToWavFile(allData, 'c.wav')

	recorder.play('c.wav')
