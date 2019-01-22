# Hardware - Lopy 4 & Pytrack

## Software
The folder *Softwares* contains the microPython codes that we created to use the Lopy 4 and the Pytrack, according to our needs for this project
In this directory, you can find:

- **boot.py**: this is the first file that the Lopy will run when booting. We used it to set the time to UTC+1 timezone.

- **main.py** which is the main file. You can find inside various functions implemented that we needed for our project. In the *main* function, the **dynamic mapping** is implemented. For this one, the Lopy will do every minute the following steps:
	- First, try to connect to a WiFi access point (*connectToWifi* function) to be able to send data to the server. 
	- Once the connection is done, it will start collecting the networks available around it and store it in a *.txt* file (*wifiRoomMappingDynamic* function). 
	- Finally, it will send the information stored in this file to the server, and specify the room in which the hardware is (*sendMappingToServer* function).  

Note that you can find other functions implemented in this file, like for example to get GPS coordinates, using the Pytrack, or to perform Bluetooth scans to collect available Bluetooth devices.

- **lib**: this folder contains all the external librairies needed. You can find:

	- **L76GNSS.py** and **pytrack.py** used to get the GPS coordinates from the GPS chip of the Pytrack.
	- **microWebCli.py** used to send the HTTP POST request to the server.


## Atom IDE & Pymakr plugin 

To develop our microPython software, we used an IDE called **Atom** (https://atom.io/).
We chose this one because there is the possibility to add a plugin called **Pymakr** which allows to download/upload directly the files from/to the Lopy and Pytrack. You can find more information about this plugin on the following website: https://pycom.io/solutions/software/pymakr/.
