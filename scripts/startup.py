import os 
import time
import threading

#os.system("sudo python /home/pi/flir_lepton_sensor/scripts/GPS.py")
#os.system("sudo python /home/pi/flir_lepton_sensor/scripts/sensor.py")

def start(i):
    if (i==0):
        time.sleep(1)
        os.system("python /home/pi/flir_lepton_sensor/scripts/GPS.py")
    elif(i==1):
        time.sleep(1)
        os.system("python /home/pi/flir_lepton_sensor/scripts/sensor.py")
    else:
        pass
for i in range(2):
    t = threading.Thread(target=start, args=(i,)) 
    t.start()
