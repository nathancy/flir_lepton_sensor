from flir_lepton_sensor import flirLepton3Sensor
import multiprocessing
from CSV_Logger import CSV_Logger

sensor = flirLepton3Sensor()
logger = CSV_Logger()

try:
    sensor.status_LED_enable()
    logger.GPS_logging_init()
    path = logger.get_path()

    while True:
        thermal_sensor = multiprocessing.Process(target=sensor.thermal_capture_record_constant_CSV_logging(path))
        thermal_sensor.daemon = True

        GPS_logger = multiprocessing.Process(target=logger.record_GPS_data(sensor.get_image_id()))
        GPS_logger.daemon = True
        thermal_sensor.start()
        GPS_logger.start()
except KeyboardInterrupt:
    print("Stopping sensor readings")
    sensor.status_LED_disable()
