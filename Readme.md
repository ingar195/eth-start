# TRex-ETH-Start

This is a script for starting and stopping mining while idle

## Installation

Install Python 3 x64 [Dowload here](https://www.python.org/downloads/)

Remember to add python to path under installation

Download Trex [Dowload here](https://github.com/trexminer/T-Rex/releases)

## Setup and config
Change line 48 and 49 in config.json
           
```json
"user": "WALLET_ADDRESS",
"worker": "WORKER_NAME"
```

Copy the trex.exe and config.json to 
```bash
C:\Program Files\EthMiner
```
## Auto launch
Create a bat file to start the python program (add a w to python (pythonw.exe) to run the program in the background)

```bash
cd C:\Program Files\EthMiner
C:\Users\%username%\AppData\Local\Programs\Python\Python39\python.exe start_eth.py 
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
