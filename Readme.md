# T-Rex ETH-Start

This is a script for starting and stopping mining while idle.

## Installation

Install Python 3 x64 [Download here](https://www.python.org/downloads/)

Remember to add python to path under installation.

Download Trex [Download here](https://github.com/trexminer/T-Rex/releases) and unpack it.

## Setup and config

Change line 2-4 in config.json to match the locations on your pc.
           
```json
    "trex_path": "path_to_trex_executable",
    "trex_log": "path_to_trex_log",
    "refreshRate": 3,
    "idleTimeReq": 10,
```
Change line 52 and 53 in config.json.
           
```json
"user": "WALLET_ADDRESS",
"worker": "WORKER_NAME",
```


## Auto launch
Create a bat file to start the python program (add a w to python (pythonw.exe) to run the program in the background)

```bash
cd C:\Program Files\EthMiner
pyw start_eth.py
```

You can also add a custom path for the config (use / not \\ )
```bash
cd C:\Program Files\EthMiner
pyw start_eth.py path/to/config/file
```



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
