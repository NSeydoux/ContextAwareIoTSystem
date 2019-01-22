from network import WLAN
from network import Bluetooth
import ubinascii
import utime
import json
from microWebCli import MicroWebCli as wc #https://github.com/jczic/MicroWebCli || https://microwebcli.hc2.fr/
from L76GNSS import L76GNSS
from pytrack import Pytrack

##############################################################################################################
### Constant Variables
##############################################################################################################
#SERVER_URL = "http://smartcampus.ddns.net:55555/testsimplequery.php"
SERVER_URL = "http://192.168.1.182/testsimplequery.php"
SERVER_LOGIN = "ISSProject"
SERVER_PWD = "ISSSmartCampus"
NB_SCAN_WIFI = 3            #Number of scan for wifi networks to perform to build the wifi payload
WIFI_DELAY_SCAN_SEC = 10    #Delay between the wifi scans
NB_SCAN_BL = 3              #Number of scan for bluetooth networks to perform to build the bluetooth payload
BL_DELAY_SCAN_SEC = 10      #Delay between the bluetooth scans

################################################################################################################
### Functionality: Connect to a wifi network.
### Params:
###     - ssid (string): ssid of the wifi network to connect
###     - auth_type: authentification system of the wifi network (None, WLAN.WEP, WLAN.WPA, WLAN.WPA2)
###     - pwd (string): security key the wifi network
################################################################################################################
def connectToWifi(ssid, auth_type, pwd):
    wlan.connect(ssid, auth=(auth_type, pwd))
    utime.sleep(5) #Wait for connexion to be establish
    while not wlan.isconnected():
        print("Connection to WiFi failed! Trying again...")
        wlan.connect(ssid, auth=(auth_type, pwd))
        utime.sleep(5) #Wait for connexion to be establish
    print("Wifi: Connection Successful!")
    #if wlan.isconnected():
    #    print("Wifi: Connection Successful!")
    #else:
    #    raise Exception("ERROR in connectToWifi - Connection Failed!")


################################################################################################################
### Functionality: Performs NB_SCAN_WIFI scans and store the wifi networks found in the wifi_networks dict.
### Param:
###     - wifi_index (int): index of the wifi networks to begin with.
### Return: wifi_networks & wifi_index.
################################################################################################################
def getWifiNetworks(wifi_index):
    wifi_networks = {}
    nb_scan = 0

    while nb_scan < NB_SCAN_WIFI:
        nets = wlan.scan() #Performs a network scan and returns a list of named tuples with (ssid, bssid, sec, channel, rssi)
        for net in nets:
            wifi_networks[str(wifi_index)] = {"id": str(ubinascii.hexlify(net.bssid, ":"))[2:19],"rssi": str(net.rssi)}
            wifi_index+=1
        nb_scan+=1
        utime.sleep(WIFI_DELAY_SCAN_SEC)

    print("getWifiNetworks - Done!")
    return wifi_networks, wifi_index


#################################################################################################################
### Functionality: Performs NB_SCAN_BL scans and store the bluetooth networks found in the bl_networks dict.
### Return: bl_networks
################################################################################################################
#https://github.com/pycom/pycom-micropython-sigfox/blob/master/docs/library/network.Bluetooth.rst
def getBluetoothNetworks():
    bl_networks = {}
    tmp_mac = []
    bl_index = 0
    nb_scan = 0

    bl = Bluetooth()
    while nb_scan < NB_SCAN_BL:
        print("scan : %d" %nb_scan)
        bl.start_scan(10) #Duration of scan to be define !!!!
        while bl.isscanning():
            adv = bl.get_adv()
            if adv:
                if adv.mac not in tmp_mac:
                    tmp_mac.append(adv.mac)
                    bl_networks[str(bl_index)] = {"id": str(ubinascii.hexlify(adv.mac, ":"))[2:19],"rssi": str(adv.rssi)}
                    print("NAME = %s -- MAC : %s -- RSSI = %d" %(bl.resolve_adv_data(adv.data, bl.ADV_NAME_CMPL), ubinascii.hexlify(adv.mac, ":"), adv.rssi))
                    bl_index+=1
        nb_scan+=1
        tmp_mac = []
        utime.sleep(BL_DELAY_SCAN_SEC)

    print("getBluetoothNetworks - Done!")
    return bl_networks


################################################################################################################
### Functionality: Send HTTP POST Request to the REST server.
### Params:
###     - url (string): url of the server
###     - login (string): login to conect to the server
###     - pwd (string): password to connect to the server
###     - wifi_payload (dict): dict that contains the wifi networks found (cf getWifiNetworks function)
###     - bl_payload (dict): dict that contains the bluetooth networks found (cf getBluetoothNetworks function)
###     - room (string): room in which the mapping is done.
###     - fromFile (bool): if true, the wifi_payload come from a file.
################################################################################################################
def sendData(url, login, pwd, wifi_payload, bl_payload, room, fromFile):
    if fromFile:
        data = {
            "login": login,
            "password": pwd,
            "signalsWifi": wifi_payload,
            "signalsBle": json.dumps(bl_payload),
            "room": room,
        }
    else:
        data = {
            "login": login,
            "password": pwd,
            "signalsWifi": json.dumps(wifi_payload),
            "signalsBle": json.dumps(bl_payload),
            "room": room
        }

    answer = wc.POSTRequest(url, formData=data)
    print(answer)

    if answer == b'Not Authorized':
        raise Exception("ERROR in sendData - Server authentification failed")
    else:
        print("Data sent!")


################################################################################################################
### Functionality: Gets and returns GPS coordinates.
### Return:
###     - coord: GPS coordinates (longitude, latitude).
################################################################################################################
def getGPSCoord():
    py = Pytrack()
    l76 = L76GNSS(py, timeout=30)
    coord = l76.coordinates(debug=True)
    while coord == (None, None):
        coord = l76.coordinates(debug=True)
        print(coord)
    return coord


################################################################################################################
### Functionality: Open a file and returns it contents.
### Params:
###     - path (string): path to file to read.
### Return:
###     - data: contents of the file.
################################################################################################################
def importDataFromFile(path):
    file = open (path, "r")
    data = file.read()
    file.close()

    return data


################################################################################################################
### Functionality: Open a file and write data in the file.
### Params:
###     - path (string): path to file to read.
###     - data: data to write in the file.
################################################################################################################
def saveDataToFile(path, data):
    file = open (path, "w")
    file.write(data)
    file.close()

################################################################################################################
### Functionality: call getWifiNetworks() every 5 minutes during 2h (= 24 times) and store the result in  file.
### Params:
###     - path (string): path to file to write.
###
################################################################################################################
def wifiRoomMappingStatic (path):
    wifi_index = 0
    wifi_networks = {}
    for nb_iterations in range (0, 24):
        nets = wlan.scan() #Performs a network scan and returns a list of named tuples with (ssid, bssid, sec, channel, rssi)
        for net in nets:
            wifi_networks[str(wifi_index)] = {"id": str(ubinascii.hexlify(net.bssid, ":"))[2:19],"rssi": str(net.rssi)}
            wifi_index+=1
        utime.sleep(300) #wait 5 minutes
        print("mapping")
    saveDataToFile(path, json.dumps(wifi_networks))


################################################################################################################
### Functionality: call getWifiNetworks() (which make 3 scans) and store the result in  file.
### Params:
###     - path (string): path to file to write.
###
################################################################################################################
def wifiRoomMappingDynamic (path):
    wifi_index = 0
    wifi_networks = {}
    nets = wlan.scan() #Performs a network scan and returns a list of named tuples with (ssid, bssid, sec, channel, rssi)
    for net in nets:
        wifi_networks[str(wifi_index)] = {"id": str(ubinascii.hexlify(net.bssid, ":"))[2:19],"rssi": str(net.rssi)}
        wifi_index+=1
    saveDataToFile(path, json.dumps(wifi_networks))


################################################################################################################
### Functionality: send the result of the wifiRoomMapping to the server.
### Params:
###     - path (string): path to file containing the networks for the mapping of the room (result of wifiRoomMapping function).
###     - room (string): room in which the mapping was done.
################################################################################################################
def sendMappingToServer(path, room):
    wifi_payload = importDataFromFile(path)
    sendData(SERVER_URL, SERVER_LOGIN, SERVER_PWD, wifi_payload, None, room, True)
    print("Data sent to the server")


################################################################################################################
################################################################################################################
if __name__ == "__main__":
    wlan = WLAN(mode=WLAN.STA)
    connectToWifi("ASUS_Wifi", WLAN.WPA2, "isssmartcampus")
    while True:
        print("Start Mapping GEI_113")
        utime.sleep(5)
        wifiRoomMappingDynamic("dynamic_mapping_gei_113.txt")
        print("Sending mapping to the server")
        sendMappingToServer("dynamic_mapping_gei_113.txt", "GEI_113")
        print("Waiting 60 secondes")
        utime.sleep(60) #wait 1 minute

    print("End!")
