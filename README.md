# Sites Monitoring Utility

This script takes a list of domains from txt file and check 
if each domain is available and paid (More than 30 days before 
expiration day).

# How to use
You need Python 3.5 or higher to be installed and modules 
from requirements.txt
You should specify each domain in txt file in new line
You might have to run python3 instead of python depending on system.

```commandline
python check_sites_health.py -h
usage: check_sites_health.py [-h] -i INPUTFILE

optional arguments:
  -h, --help            show this help message and exit
  -i, --inputfile       Path to txt file with list of domains. 
                        Required parameter

```
```commandline
Example:
input file domains.txt:
https://vk.com
https://google.com
https://github.com

python check_sites_health.py -i domains.txt

https://vk.com is active and paid
https://google.com is active and paid
https://github.com is active and paid

```


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
