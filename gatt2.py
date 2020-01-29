import pexpect
import time
import json
import sys
import struct
#DEVICE="30:AE:A4:58:E2:62"
#DEVICE= "D8:A0:1D:40:A5:5E"
DEVICE = "80:7D:3A:C3:26:C6"
#DEVICE= "24:0A:C4:0D:16:F6"
#print("Boreal Bikes Server address:")
#print(DEVICE)

#Run gatttool interactively
#print("Run gatttool..")

#child = pexpect.spawn("gatttool -t random -b "+DEVICE+ " -I")
child = pexpect.spawn("gatttool -I")

child.sendline("disconnect")
child.sendline("connect {0}".format(DEVICE))
child.expect("Connection successful", timeout=5)


#print("Connected")

#function to transform hex string into integer

def hexStrToInt(hexstr):
    val = int(hexstr.replace(" ",""), 16)
    return val


#function to hex value from characteritcs

#uuids = ["42427a02-0000-1000-8000-005a45535953","0000baaa-1212-efde-1523-785fef13d123",
 #"0000beee-1212-efde-1523-785fef13d123", 
#"42427a08-0000-1000-8000-005a45535953", "42427a07-0000-1000-8000-005a45535953",
 #"42427a06-0000-1000-8000-005a45535953" ,"42427a01-0000-1000-8000-005a45535953","42427a10-0000-1000-8000-005a45535953", "42427a11-0000-1000-8000-005a45535953"]
uuids = ["0000beee-1212-efde-1523-785fef13d123"]
def getHexValues(uuid):
    if uuid == "0000beee-1212-efde-1523-785fef13d123":
        #lockcontrol write 1 or 0
        counter = len(sys.argv)
        if counter == 2:
            val = int((sys.argv)[1])
            if val == 40 or val == 41:
            #print(val)
                command = "char-write-req 0x003d "+str(val)
                #print(command)
                child.sendline(command)
                child.expect("Characteristic value was written successfully", timeout=10)

def getArgs(arg):
    counter = len(arg)
    if counter == 2:
        val = int(arg[1])
        if val == 40 or val == 41:
            #print(val)
	    print("ok")
        
for uuid in uuids:
    getHexValues(""+uuid)

#getArgs(sys.argv)

