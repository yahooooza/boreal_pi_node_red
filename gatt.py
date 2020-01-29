import pexpect
import time
import json
import sys
import struct

DEVICE="80:7D:3A:C3:26:C6"
child = pexpect.spawn("gatttool -I")
child.sendline("disconnect")
child.sendline("connect {0}".format(DEVICE))
child.expect("Connection successful", timeout=5)

def hexStrToInt(hexstr):
    val = int(hexstr.replace(" ",""), 16)
    return val

uuids = ["42427a06-0000-1000-8000-005a45535953", "42427a08-0000-1000-8000-005a45535953", "0000baaa-1212-efde-1523-785fef13d123",
 "42427a02-0000-1000-8000-005a45535953", "42427a10-0000-1000-8000-005a45535953", "42427a11-0000-1000-8000-005a45535953" , "42427a01-0000-1000-8000-005a45535953"]
def getHexValues(uuid):
    if uuid == "42427a02-0000-1000-8000-005a45535953":
        #bms and  motor
       child.sendline("char-read-uuid "+ uuid)
       child.expect("value:", timeout=10)
       child.expect("\r\n", timeout=10)
       percent = hexStrToInt(child.before[1:3])
       print("\"Percent\": "+str(percent)+",")
       batVol = hexStrToInt(child.before[4:10])
       print("\"Battery Total Voltage\": "+ str(batVol)+",")
       datet = hexStrToInt(child.before[10:22])
       print("\"Time & Date\": "+str(datet)+",")

       speed = hexStrToInt(child.before[22:25])
       print("\"Speed\": "+str(speed)+",")
       motVol = hexStrToInt(child.before[25:30])
       print("\"Motor Total Voltage\": "+str(motVol)+",")
       distance = hexStrToInt(child.before[31:36])
       print("\"Distance\": "+str(distance) + ",")
    if uuid == "0000baaa-1212-efde-1523-785fef13d123":
        #ilockit
        child.sendline("char-read-uuid "+ uuid)
        child.expect("value:", timeout=10)
        child.expect("\r\n", timeout=10)
        lockstate = hexStrToInt(child.before[1:3])
        print("\"Lockstate\": "+str(lockstate)+",")
	sessiontime = hexStrToInt(child.before[16:21])
        print("\"Sessiontime\": "+str(sessiontime)+",")
    elif uuid == "0000beee-1212-efde-1523-785fef13d123":
        #lockcontrol write 1 or 0
        counter = len(sys.argv)
        if counter == 2 or counter == 3:
            val = int((sys.argv)[1])
            if val == 40 or val == 41:
                command = "char-write-req 0x003d "+str(val)
                child.sendline(command)
                child.expect("Characteristic value was written successfully", timeout=10)
    elif uuid == "42427a01-0000-1000-8000-005a45535953":
        child.sendline("char-read-uuid "+ uuid)
        child.expect("value:", timeout=10)
        child.expect("\r\n", timeout=10)
        beats = hexStrToInt(child.before[1:3])
        print("\"Beats\": "+str(beats)+",")
        datet = hexStrToInt(child.before[3:15])
        print("\"Time & Date(Heart)\": "+str(datet)+"}")
    elif uuid == "42427a08-0000-1000-8000-005a45535953":
        #LORA info
        child.sendline("char-read-uuid "+ uuid)
        child.expect("value:", timeout=10)
        child.expect("\r\n", timeout=10)
        loraInfo = hexStrToInt(child.before[1:13])
        print("\"Lora Info\": "+str(loraInfo)+",")

    elif uuid == "42427a07-0000-1000-8000-005a45535953":
        counter = len(sys.argv)
        if counter == 3:
            val = int((sys.argv)[1])
            command = "char-write-req 0x003c "+str(val)
            child.sendline(command)
            child.expect("Characteristic value was written successfully", timeout=10)

    elif uuid == "42427a06-0000-1000-8000-005a45535953":
        child.sendline("char-read-uuid "+ uuid)
        child.expect("value:", timeout=10)
        child.expect("\r\n", timeout=10)
        currtime = hexStrToInt(child.before[1:13])
        print("{\"ESP32 Current Time\": "+str(currtime)+",")

    elif uuid == "42427a10-0000-1000-8000-005a45535953":
        child.sendline("char-read-uuid "+ uuid)
        child.expect("value:", timeout=10)
        child.expect("\r\n", timeout=10)
        prelat = child.before[1:13]
        characlat = prelat.replace(" ","")
        lat = struct.unpack('!f', characlat.decode('hex'))[0]
        print("\"Latitude\": "+str(format(lat, '.6f'))+",")
        pre = child.before[13:25]
        charac = pre.replace(" ","")
        lon = struct.unpack('!f', charac.decode('hex'))[0]
        print("\"Longitude\": "+str(format(lon, '.6f'))+",")
        preElev = child.before[25:37]
        charelev = preElev.replace(" ","")
        elevation  = struct.unpack('!f', charelev.decode('hex'))[0]
        print("\"Elevation\": "+str(format(elevation,'.2f'))+",")
        datet = hexStrToInt(child.before[37:49])
        print("\"Time & Date(Location)\": "+str(datet)+",")
    elif uuid == "42427a11-0000-1000-8000-005a45535953":
        child.sendline("char-read-uuid "+ uuid)
        child.expect("value:", timeout=10)
        child.expect("\r\n", timeout=10)
        crashD = hexStrToInt(child.before[1:3])
        print("\"Crash\": "+str(crashD)+",")
        dateT1 = hexStrToInt(child.before[3:15])
   
        print("\"Time & Date (MPU)\": "+str(dateT1)+",")
        

def getArgs(arg):
    counter = len(arg)
    if counter == 2:
        val = int(arg[1])
        if val == 40 or val == 41:
            #print(val)
	    print("ok")
        
for uuid in uuids:
    getHexValues(""+uuid)


