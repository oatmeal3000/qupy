
from django.conf.urls import include, url
from .views import audioDemo, cameraDemo, driveCar, soundRanging, lightSensing, tempSensing, home, soundSensing, gpioControl

urlpatterns = [
    url(r'^$', home),
    url(r'^temp$', tempSensing),
    url(r'^audio$', audioDemo),
    url(r'^camera$', cameraDemo),
    url(r'^drive_car$', driveCar),
    url(r'^sound_ranging$', soundRanging),
    url(r'^light_sensing$', lightSensing),
    url(r'^sound_sensing$', soundSensing),
    url(r'^gpio$', gpioControl),
]
