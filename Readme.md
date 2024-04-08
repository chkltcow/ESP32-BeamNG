# ESP32-BeamNG
A quick parser for BeamNG OutGauge data (will work with Live For Speed too) in MicroPython.  I was bored over the weekend and wanted to display in-game data on ESP32 hardware and couldn't find any good examples of it.  

There are a billion and one tutorials on the internet for hooking up various displays, LEDs, etc to the ESP32 so those won't be covered here.  This is just parsing the data and consolidating the documentation about it in one place.

Data on the OutGauge struct for BeamNG is at https://documentation.beamng.com/modding/protocols/

MicroPython struct.unpack documentation:  https://docs.micropython.org/en/latest/library/struct.html