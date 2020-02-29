# EKG/EMG Reader
## Python interface for Olimex SHIELD-EKG-EMG. 


![Screenshot from 2020-02-29 00-44-42](https://user-images.githubusercontent.com/25719985/75595767-fd03e180-5a8d-11ea-9a98-12b9845fd5dc.png)

This simple python module has been designed to interface with an Olimex SHIELD-EKG-EMG connected to an Arduino via serial. The aim of this project is to create a open source alternative inteface given that I was not able to find any other open source alternatives for linux. (However this should work on Windows as well)

### Dependencies

To run this project you will need to install pyserial and matplotlib by writing on your command line:

```bash
pip3 install pyserial
pip3 install matplotlib
```

### How to use

Then to run a demo use (changing the serial port if needed):

```bash
python3 EkgEmgViewer.py -p /dev/ttyACM0 -b 57600
```

The project can also be used just as a serial reader/parser, just import the module like so:

```python
from EkgEmgReader import EkgEmgReader
```

then:

```python
#Create a serial object
ekgSer=EkgEmgReader.serial_ekg(port=args.port,baudrate=args.baud,timeout=1)

#From here on its a good idea to use a loop
#Read a serial package communication
ekgSer.read_packet()
        #If there was no reading error print the package count and the X channels value
        if not ekgSer.packet.read_error:
            print(ekgSer.packet.packet_count)
            print(ekgSer.packet.channel)

```

### Contribute
Feel free to send a pull request my way or fork the repo. If this helps you create something cool I'd appreciate if you let me know.

---
Shield and other resources: https://www.olimex.com/Products/Duino/Shields/SHIELD-EKG-EMG/open-source-hardware