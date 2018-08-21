from flir_lepton_sensor import flirLepton3Sensor

sensor = flirLepton3Sensor()
try:
    sensor.thermal_capture_record_constant()
except KeyboardInterrupt:
    print("Stopping sensor readings")

