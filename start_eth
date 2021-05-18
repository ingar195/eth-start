import os
# Install dependencies
depList = ["colorama"]
for item in depList:
    os.system("py -m pip install {}".format(item))
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
    print(Fore.YELLOW + "Time were greater than {}, starting mining".format(idleTimeReq))
    os.system("start " + '"" ' + '"C:\\Program Files\\EthMiner\\t-rex.exe"' + "  --autoupdate -a ethash --url stratum+tcp://eu1.ethermine.org:4444 --user 0xbd841C01C749EAFed0aebeb84d0edd99171E65Af --pass x --worker %COMPUTERNAME%")

def kill(idleTimeReq):
	print(Fore.RED + "Stopping mining since idle time were less than {}".format(idleTimeReq))
	os.system("taskkill /F /IM T-REX*")

def main():
	print("Starting")
	idleTimeReq = 1   # Idle time before start in Seconds
	refreshRate = 60    # How often to check in Seconds
	mining = False
	msg = False
	while True:
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
			kill(idleTimeReq)
			mining = False
		print("Waiting {} seconds to check again".format(refreshRate))
		print(" ")
		time.sleep(refreshRate)

#Run Script
if __name__ == "__main__":
	try:
		init(autoreset=True)
		main()
	except KeyboardInterrupt:
		kill("600")
		print ("Script Interrupted")


    
