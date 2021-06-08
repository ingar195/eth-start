# Load and Install dependencies
import os
import time
import subprocess
import requests

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

def run(idleTimeReq):
    print(Fore.YELLOW + "Time were greater than {} Seconds, starting mining".format(idleTimeReq))
    os.system("start " + '"" ' + '"C:\\Program Files\\EthMiner\\t-rex.exe"' + "  -c config.json")

def kill(idleTimeReq, interrupted):
	try:
		subprocess.run('taskkill /IM t-rex.exe', check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
		print(Fore.RED + "Stopping mining since idle time were less than {} Seconds".format(int(idleTimeReq)))
	except:
		pass

def getHashRate():
	url = "http://127.0.0.1:4067/summary"
	try:
		response = requests.get(url)	
		data = response.json()
		hashRate = data["hashrate"]/1000000
		print(Fore.GREEN +"{} MH/s".format(hashRate)) 
	except:
		print("No communication with miner")
		hashRate = 0
	return hashRate

def main():
	print("Starting")
	idleTimeReq = 5   # Idle time before start in Seconds
	refreshRate = 1    # How often to check in Seconds
	mining = False
	msg = False
	while True:
		getHashRate()
		print(Fore.GREEN + "Idle time = {}".format(getIdleTime()))
		if getIdleTime() >= idleTimeReq:
			if mining == False:
				run(idleTimeReq)
				mining = True
			else:
				if msg == False:
					print(Fore.YELLOW + "Mining already running, not staring")
					msg = True
		elif getIdleTime() <= idleTimeReq and mining == True:
			kill(idleTimeReq,False)
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


    