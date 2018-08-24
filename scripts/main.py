from flir_lepton_sensor import flirLepton3Sensor

sensor = flirLepton3Sensor()
try:
    sensor.status_LED_enable()
    sensor.thermal_capture_record_constant_CSV_logging()
except KeyboardInterrupt:
    print("Stopping sensor readings")
    sensor.status_LED_disable()

