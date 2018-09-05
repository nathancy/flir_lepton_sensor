# flir_lepton_sensor

Python module for capturing images from the Lepton over SPI (for example, on a Raspberry PI). Uses the Pylepton library for thermal image capture. Integrates GPS coordinates with corresponding thermal image and CSV logging. Contains scripts to convert CSV data into KML to be used with Google Earth image processing.

## Installation and Dependencies
Requires `cv2` and `numpy` modules. To install:
```
sudo apt-get install python-opencv python-numpy
```

Next, to install into site-packages for distribution through a distutils setup:
```
cd library
sudo python setup.py install
```

## Example Usage

Capture a single frame

```
import numpy as np
import cv2
from pylepton.Lepton3 import Lepton3

with Lepton3() as l:
  a,_ = l.capture()
cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX)  # Extend contrast
np.right_shift(a, 8, a)                         # Fit data into 8 bits
cv2.imwrite("output.jpg", np.uint8(a))          # Write it
```

Image data from `capture()` is 12-bit, non-normalized (raw sensor data). Here we contrast extend it since the bandwidth tends to be narrow.

`capture()` returns a tuple that includes a unique frame ID, as lepton frames can update at ~27 Hz, but only unique ones are returned at ~9 Hz. Currently, this is just a simple sum, but ideally this will turn into a real frame ID from telemetry once this feature is implemented.

Note also that the Lepton contructor can take as an optional argument the SPI device on which to find the Lepton. If in your system that device is `/dev/spidev0.1`, you can instantiate lepton as such:

```
with Lepton("/dev/spidev0.1") as l:
```

## Scripts

### GPS.py and sensor.py

This program will constantly capture thermal images and log the current GPS coordinates in a CSV file with the corresponding location where the image was taken. These are two separate programs that run independently. Run `GPS.py` then `sensor.py` in two separate terminals. Image output is placed into the `photos` directory where sessions are separated by timestamp. These two scripts are run on bootup on the Raspberry Pi using Cron.

### capture.py

This program will output any image format that opencv knows about, just specify the output file format extension (e.g. `output.jpg` or `output.png`)

To capture a png file named `output.png`:
```
python capture.py output.png
```

To view additional options/settings:
```
python capture.py --help
```

Additional settings are:
```
Usage: pylepton_capture [options] output_file[.format]

Options:
  -h, --help           show this help message and exit
  -f, --flip-vertical  flip the output image vertically
```

### overlay.py

Requires `python-picamera`, a Raspberry PI, and compatible camera.
```
sudo apt-get install python-picamera
```

To get a 100% lepton overlay (note camera installation still required):
```
python overlay -a 255
```

To view additional options/settings:
```
python overlay.py --help
```

Additional settings are:
```
Usage: pylepton_overlay [options]

Options:
  -h, --help               show this help message and exit
  -f, --flip-vertical      flip the output images vertically
  -a ALPHA, --alpha=ALPHA  set lepton overlay opacity
```

### KML_generator.py

This script will convert CSV data into KML for usage with Google Earth image processing. Resolution/Placemark density can be set by giving the script an argument. The default resolution is create a Placement for every line in the CSV file (with each line equivalent to 1 sample a second). Ex: Resolution = 10 means one Placemark point for every 10 lines in the CSV file.

To convert CSV data into KML file:
```
python KML_generator.py [resolution]
```

Example: To generate a Placemark every 10 seconds
```
python KML_generator.py 10
```
