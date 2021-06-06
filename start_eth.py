# Load and Install dependencies
import os
import time
import subprocess
from urllib import request

try:
	subprocess.run("py -m pip install colorama", check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except Exception as e:
	print (e)
	exit()
from colorama import Fore, init
from ctypes import Structure, windll, c_uint, sizeof, byref, c_ulong


class LASTINPUTINFO(Structure):
	_fields_ = [
		('cbSize', c_uint),
		('dwTime', c_uint),
	]

def getIdleTime():
	lastInputInfo = LASTINPUTINFO()
	lastInputInfo.cbSize = sizeof(lastInputInfo)
	windll.user32.GetLastInputInfo(byref(lastInputInfo))
	getTickcount = c_ulong(windll.kernel32.GetTickCount64())
	idleTime = getTickcount.value - lastInputInfo.dwTime
	return idleTime / 1000.0


def startMiner():
    os.system("start " + '"" ' + '"C:\\Program Files\\EthMiner\\t-rex.exe"' + " -c config.cfg")


def gpuControl(enable, selectedGPU):
	request.urlopen("http://127.0.0.1:4067/control?pause={}:{}".format(enable, selectedGPU))


def main():
	print("Starting")
	idleTimeReq = 5   # Idle time before start in Seconds
	refreshRate = 1    # How often to check in Seconds
	mining = False
	msg = False
	startMiner()
	while True:		
		print(Fore.GREEN + "Idle time = {}".format(getIdleTime()))
		if getIdleTime() >= idleTimeReq:
			if mining == False:
				
				print(Fore.GREEN + "Un pause mining since idle time were less than {} Seconds".format(int(idleTimeReq)))
				gpuControl("false", "0")
				mining = True
			else:
				if msg == False:
					print(Fore.YELLOW + "Mining already running, not staring")
					msg = True
		elif getIdleTime() <= idleTimeReq and mining == True:
			print("Pause mining")
			print(Fore.RED + "Pauseing mining since idle time were less than {} Seconds".format(int(idleTimeReq)))

			gpuControl("true", "0")
			(idleTimeReq,False)
			mining = False
		print("Waiting {} seconds to check again\n".format(refreshRate))
		time.sleep(refreshRate)




#Run Script
if __name__ == "__main__":
	try:
		init(autoreset=True)
		main()
	except KeyboardInterrupt:
		kill(None,True)
		print ("Script Interrupted")


    
