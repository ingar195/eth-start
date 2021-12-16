# Load and Install dependencies
import os
import time
import subprocess
import requests
import psutil
import logging

try:
    subprocess.run("py -m pip install colorama", check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except Exception as e:
    logging.error(e)
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
    logging.debug("Time were greater than {} Seconds, starting mining".format(idleTimeReq))
    os.system("start " + '"" ' + '"C:\\Users\\ingar\\Documents\\Mining\\t-rex.exe"' +
              "  -c config.json --api-bind-http 0.0.0.0:4067")


def kill(idleTimeReq, interrupted):
    try:
        subprocess.run('taskkill /IM t-rex.exe', check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logging.debug("Stopping mining since idle time were less than {} Seconds".format(int(idleTimeReq)))
    except:
        pass


def getHashRate():
    url = "http://127.0.0.1:4067/summary"
    try:
        response = requests.get(url)
        data = response.json()
        hashRate = data["hashrate"]/1000000
        logging.debug("{} MH/s".format(hashRate))
    except:
        logging.debug("No communication with miner")
        hashRate = 0
    return hashRate


def CheckRunningPrograms():

    processes = psutil.process_iter()
    blacklist = []
    # Read Blacklist file
    with open(r"D:\Workspace\eth-start\blacklist.txt", "r") as f:
        for line in f.readlines():

            if line != "" or line != "\n":
                line = line.strip("\n")
                blacklist.append(line.lower())
    # Checks if program in blacklist is running
    for p in processes:
        pName = p.name().lower()
        if pName in blacklist:
            logging.debug(f"{pName} is running")
            return True


def main():
    logging.debug("Starting")
    idleTimeReq = 5  # Idle time before start in Seconds
    refreshRate = 3    # How often to check in Seconds
    mining = False
    msg = False
    while True:
        getHashRate()
        logging.info("Idle time = {}".format(getIdleTime()))
        if getIdleTime() >= idleTimeReq:
            if mining == False:
                run(idleTimeReq)
                mining = True
            else:
                if msg == False:
                    logging.info("Mining already running, not staring")
                    msg = True
        elif getIdleTime() <= idleTimeReq and mining == True:
            blacklist = CheckRunningPrograms()
            if blacklist:
                logging.debug("Program in blacklist running")
                kill(idleTimeReq, False)
                mining = False
        logging.info("Waiting {} seconds to check again".format(refreshRate))
        time.sleep(refreshRate)


# Run Script
if __name__ == "__main__":

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%d-%m-%Y:%H:%M:%S',
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler("start_eth.log"),
            logging.StreamHandler()
        ])

    try:
        main()
    except KeyboardInterrupt:
        kill(None, True)
        logging.error("Script Interrupted")
