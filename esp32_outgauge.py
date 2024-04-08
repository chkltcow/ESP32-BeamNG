import esp
esp.osdebug(None)
import gc
gc.collect()
import network
import socket
import struct

def parseOutGauge(data):
    # Other documentation I found online uses the unpack string "I4sH2c7f2I3f16s16si".
    # MicroPython doesn't support "c" as an unpack character, so we use "ss"
    return struct.unpack("I4sHss7f2I3f16s16si", data)

def printDebug(telemetry):
    # Via https://documentation.beamng.com/modding/protocols/
    # typedef struct xxx {
    #     unsigned       time;            // time in milliseconds (to check order) // N/A, hardcoded to 0
    #     char           car[4];          // Car name // N/A, fixed value of "beam"
    #     unsigned short flags;           // Info (see OG_x below)
    #     char           gear;            // Reverse:0, Neutral:1, First:2...
    #     char           plid;            // Unique ID of viewed player (0 = none) // N/A, hardcoded to 0
    #     float          speed;           // M/S
    #     float          rpm;             // RPM
    #     float          turbo;           // BAR
    #     float          engTemp;         // C
    #     float          fuel;            // 0 to 1
    #     float          oilPressure;     // BAR // N/A, hardcoded to 0
    #     float          oilTemp;         // C
    #     unsigned       dashLights;      // Dash lights available (see DL_x below)
    #     unsigned       showLights;      // Dash lights currently switched on
    #     float          throttle;        // 0 to 1
    #     float          brake;           // 0 to 1
    #     float          clutch;          // 0 to 1
    #     char           display1[16];    // Usually Fuel // N/A, hardcoded to ""
    #     char           display2[16];    // Usually Settings // N/A, hardcoded to ""
    #     int            id;              // optional - only if OutGauge ID is specified
    # } xxx;
    gear = int.from_bytes(telemetry[3], "big")
    
    speed = telemetry[5] # in m/s
    speedMPH = speed * 2.237
    speedKPH = speed * 3.6
    
    rpm = telemetry[6]
    
    boostBar = telemetry[7]
    boostPSI = boostBar * 14.50377377337509
    
    waterTempC = telemetry[8]
    waterTempF = (waterTempC * 1.8) + 32
    
    fuel = telemetry[9]
    
    oilTempC = telemetry[11]
    oilTempF = (oilTempC * 1.8) + 32
    
    throttle = telemetry[14]
    brake = telemetry[15]
    clutch = telemetry[16]
    
    print("Gear: {:2d}   Boost: {:2.2f} PSI".format(gear, boostPSI))
    print("{:3.0f} MPH   {:5.0f} RPM".format(speedMPH, rpm))
    print("Temps - Water: {:3.1f}F    Oil: {:3.1f}F".format(waterTempF, oilTempF))
    



# Set up WLAN connection
ssid = 'MY_SSID'
password = 'MY_PSK'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

# Okay we connected to WiFi.  Listen for UDP connection from BeamNG
port = 4444
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = station.ifconfig()[0]
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) 
s.bind((ip,port)) 
print("Listening on udp://{}:{}".format(ip, port))

# Main loop - receive data from BeamNG and do something with it
while True:
    data,addr=s.recvfrom(96)
    telemetry = parseOutGauge(data)
    printDebug(telemetry)

