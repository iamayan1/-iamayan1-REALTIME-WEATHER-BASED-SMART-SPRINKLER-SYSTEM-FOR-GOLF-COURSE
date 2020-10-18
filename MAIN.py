import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
#Provide your IBM Watson Device Credentials
organization = "0l9u76"
deviceType = "device"
deviceId = "12345"
authMethod = "token"
authToken = "12345678"

# Initialize GPIO

def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)
        print(type(cmd.data))
        i=cmd.data['command']
        if i=='moteron':
                print("moter is on")
        else:
                print("moter is off")
        

try:
        deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
        deviceCli = ibmiotf.device.Client(deviceOptions)
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()


deviceCli.connect()

while True:
        
        hum=random.randint(30,100)
        temp = random.randint(30,150)
        moisture= random.randint(0,100)
        #Send Temperature & Humidity to IBM Watson
        data = { 'Temperature' : temp, 'Humidity': hum, 'Soilmoisture' : moisture}
        #print (data)
        def myOnPublishCallback():
            print ("Published Temperature = %s C" %temp, "Humidity = %s %%" %hum,"Soiloisture= %s" %moisture,"to IBM Watson")

        success = deviceCli.publishEvent("DHT11", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTP")
        time.sleep(2)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
