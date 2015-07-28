var navigator = window.navigator;
var Context = window.AudioContext || window.webkitAudioContext;
var context = new Context();

// audio
var mediaStream;
var rec;

navigator.getUserMedia = (
  navigator.getUserMedia ||
    navigator.webkitGetUserMedia ||
    navigator.mozGetUserMedia ||
    navigator.msGetUserMedia
);

function record() {
  if (rec == undefined) {
  	navigator.getUserMedia({audio: true}, function(localMediaStream){
      mediaStream = localMediaStream;
      mediaStreamSource = context.createMediaStreamSource(localMediaStream);
      rec = new Recorder(mediaStreamSource, {
        workerPath: '/static/js/recorder_js/recorderWorker.js',
		outputSampleRate: 8000,
      });
      rec.record();
     }, function(err){
      console.log('Not supported');
     });
  } else {
  	rec.clear();
  	rec.record();
  }
}

function stop() {
  //mediaStream.stop();
  rec.stop();

  rec.exportWAV(function(e){
    //rec.clear();
    //Recorder.forceDownload(e, "test.wav");
	Recorder.sendToServer(e, "/demo/audio", function(html) {
		//alert(html);
		e = document.getElementById('command_text');
		e.innerHTML = html
	});
  });
}
