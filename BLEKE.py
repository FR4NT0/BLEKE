
import argparse, ctypes, sys, winreg, os

#------------------------------------------------------------------------------------------------------------------------
 
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def check_privileges(): #Checks if it is running with administrator privileges."

    if is_admin():
        print("System admin privileges granted.")
    else:
        print("Sorry, system admin privileges required to run this program.ñ")
        sys.exit(1)
#------------------------------------------------------------------------------------------------------------------------#
# List all the values present in the device registry and store the main ones
# When checking on device it gets the pairing keys
# When checking on controller gets the classic BT paired devices

def get_info(device):
    k = 0
    try:   
        #Opens the Windows registry entry for the paired devices information
        #cmd command: REG QUERY HKLM\SYSTEM\CurrentControlSet\Services\BTHPORT\Parameters\Devices
        info_reg = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
        "SYSTEM\\CurrentControlSet\\Services\\BTHPORT\\Parameters\\Devices\\" + device)
       
        name = "" # Name of the value: 'Name'
        data = [] # Contains the data of the value ('Name', b'BT5.2 Mouse\x00', 3) 
        info = {'MAC':device.upper(),'Name':'', 'Appearance':'', 'AddressType': '', 'VID':'', 'PID':'', 'Version':'', 'Services':''}   
        #print (info)
        
        #Retrieve and prints every info values of the paired BLE device in the system
    
        #Info LOOP checking all the values of the registry key
        for k in range(winreg.QueryInfoKey(info_reg)[1]):   
            # data = ('Name', b'BT5.2 Mouse\x00', 3)         
            data = winreg.EnumValue(info_reg, k)
                     
            # name= winreg.EnumValue(key_reg, k)[0] = 'LTK'
            name = data[0] #Name of the value

            # Depends on the info entry it´s stored
            match name: 
                case 'LEName':
                    info['Name'] = data[1].decode(encoding='ascii',errors='strict').rstrip('\x00')
                case 'Name':
                    if info['Name'] == '' : # Only store if no LEName found
                        info[name] = data[1].decode(encoding='ascii',errors='strict').rstrip('\x00')
                case 'LEAppearance': 
                    info['Appearance'] = hex(data[1])                 
                case 'LEAddressType': 
                    info['AddressType'] = "public" if (winreg.QueryValueEx(info_reg, 'LEAddressType')[0])== 0 else "static"                     
                case 'VID':
                    info['VID'] = data[1]
                case 'PID':
                    info['PID'] = data[1]
                case 'Version':
                    info['Version'] = data[1]
                case 'Services':
                    print ("Services")
 
            print ("    Info", data) # Print all info on screen   
        
        # Closing info registry
        winreg.CloseKey(info_reg)
        #print ("    *Closing info registry for device")    
    except WindowsError:
        print("Error accessing registry")     
    if k == 0:
        print("    No info found for this device")        
    k = 0    

    try:
        #Opens the Windows registry entry for the paired BLE devices services information
        #cmd command: REG QUERY HKLM\SYSTEM\CurrentControlSet\Services\BTHPORT\Parameters\Devices
        services_reg = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
        "SYSTEM\\CurrentControlSet\\Enum\\BTHLEDevice")

        #Prints the info values of the paired BLE device in the system
        services = ""        
        print ("    Info ('Services'", end="")
        #Info LOOP checking all the services associated with the device
        for k in range(winreg.QueryInfoKey(services_reg)[0]):        
            data = winreg.EnumKey(services_reg,k) #{00001800-0000-1000-8000-00805f9b34fb}_Dev_VID&02045e_PID&0827_REV&0103_dfe5b10bb604
                
            if device in data: #If the device is present in any of the services registered it saves it
                services = data.split('_')[0] #Keeps the first chain with service info
                print (", ", services[+1:-1], sep="", end="") #On screen
                info['Services'] += services[+1:-1] + ";" #Store the service with the comma

    except WindowsError: #If no service for the device
        print("Error accessing registry")     
        info['Services'] = ""
    if k == 0:
        print("    No services found for this device")
        
    print (")")       
    info['Services'] = info['Services'][:-1] # Removes the "; " when at the end  

    #Closing registry key
    winreg.CloseKey(services_reg)
    #print ("    *Closing services registry for device")

    print("    *Formated info:", info) 
    print ("    +")   
       
    return info
                    
#------------------------------------------------------------------------------------------------------------------------#
# List the keys present in the device registry and store the main ones
# When checking on device it gets the pairing keys
# When checking on controller gets the classic BT paired devices

def get_keys(controller, device):
    k = 0
    try:
        #Opens the Windows registry entry for the paired devices to read their keys
        #cmd command: REG QUERY HKLM\SYSTEM\CurrentControlSet\Services\BTHPORT\Parameters\Keys\e8d0fcda1084\1308ac000a96
        key_reg = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
        "SYSTEM\\CurrentControlSet\\Services\\BTHPORT\\Parameters\\Keys\\" + controller + '\\' + device)
        
        name = "" # Name of the key
        key = [] # Contains the key
        keys = {'MAC':device.upper(),'LTK':'','EDIV':'', 'ERand':'','KeyLength':''}
        master_keys = ['LTK', 'IRK', 'CSRKInbound', 'CSRK'] #Valuable keys
        other_keys = ['EDIV', 'ERand', 'KeyLength']
        
        #Prints the keys of the paired BLE device in the system
        #Keys LOOP
        for k in range(winreg.QueryInfoKey(key_reg)[1]):
                    
            # Whole key= winreg.QueryValueEx(key_reg, 'LTK')[0]= b'q\x8d\x19p\x08\xa1m\xfa\x03m\x0e\xf5=\xaf\xfb\xb8'; 
            key = winreg.EnumValue(key_reg, k) 
            
            # name= winreg.EnumValue(key_reg, k)[0] = 'LTK'
            name = key[0] #Name of the value
                  
            #Check if key is bytes format to convert it
            if (name in master_keys) : #If the name of the value is one of the master keys
                print ("    Keys* ('", name,"', ", key[1].hex().upper(),", ", key[2], ")",sep='') #Standard format of key
                #Stores key. 
                keys[name] = key[1].hex().upper() 
            elif (name in other_keys) : #If the name of the value is one of the other keys-> print and save
                print ("    Keys* ", key) 
                #Stores key. 
                keys[name] = key[1]                                                           
            else:
                print ("    Keys ", key) 
                            
        # Closing reg key
        winreg.CloseKey(key_reg)
        #print ("    *Closing keys registry for device")
    except WindowsError:
        print("Error accessing registry")
    
    if k == 0:
        print("No keys found for this device")                        
            
    print("    *Formated keys:", keys) 
        
    return keys                
#------------------------------------------------------------------------------------------------------------------------#
# List the info present in the device registry and store the main ones for classic BT
# Also gets the pairing key called LinkKey
def get_classic_devices(controller):

    k = 0
    try: #Protection in case a wrong access to registry

        #Opens the Windows registry entry for the paired devices to read their keys
        #cmd command: REG QUERY HKLM\SYSTEM\CurrentControlSet\Services\BTHPORT\Parameters\Keys\e8d0fcda1084\1308ac000a96
        key_reg = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
        "SYSTEM\\CurrentControlSet\\Services\\BTHPORT\\Parameters\\Keys\\" + controller)
        
        if os.path.exists('classicdevices.txt'): #Reseting file if exists
            os.remove('classicdevices.txt')
        basicdeviceslogfile = open('classicdevices.txt', 'a')  #Opens in append mode a file to store every device info for all devices
    
        data = [] #data from registry
         
        #Prints the keys of the paired devices in the system
        print ("   Classic paired devices")
        
        #k = 1  First entry of the registry is the 'MasterIRK' for the system so it´s discarded       
        for k in range(1,winreg.QueryInfoKey(key_reg)[1]): #loop to get all the values
        
            #data = winreg.QueryInfoKey(key_reg)#= (n subkeys, n values, last write time)
            #print("data", data)
                    
            data = winreg.EnumValue(key_reg, k)            
            #device = data[0]
            
            info = {'MAC':'','Name':'','VID':'', 'PID':'','Version':'','Appearance':'','Services':'', 'LinkKey': ''}   #Contains device info  
            #Formating name to be store in the file, unfortunately Windows doesn´t allow file and folders to have a name with ":"
            controller_name =":".join(controller[i:i+2] for i in range(0, len(controller), 2)).upper() #XX:XX:XX:XX:XX Windows doesn´t let saving this name for a folder
            device_name = ":".join(data[0][i:i+2] for i in range(0, len(data[0]), 2) ).upper()  #XX:XX:XX:XX:XX
                   
            print ("****Device ", k,": ", device_name, " *****\n", sep="")
            #LinkKey = data [1].hex().upper()                                   
            info['LinkKey'] = data[1].hex().upper() #Get the pairing key calles LinkKey            
            #print ("Device info:", info)          
            info.update(get_info(data[0])) #Get info about device through the function            
            #print ("    Device info:", info, "\n")
                      
            print("\n-------------",os.path.join( controller_name, device_name), "-------------" )

            file_content = ("[General]\nName=" + info['Name'] #Content of the device file
            + "\nClass=0x240404"
            + "\nAddressType=public"
            + "\nSupportedTechnologies=BR/EDR;LE;"
            + "\nTrusted=true"
            + "\nBlocked=false"
            + "\nServices="
            + "\n\n[LinkKey]\nKey=" + str(info['LinkKey'])
            + "\nType=4"
            + "\nPINLength=0" 
            + "\n\n[DeviceID]\nSource=1"
            + "\nVendor=" +  str(info['VID'])
            + "\nProduct=" +  str(info['PID'])
            + "\nVersion=" +  str(info['Version'])) 
                
            print("File Content", file_content)
            print("----------------------------------------------------------------")
            
            basicdeviceslogfile.write("\n**************" + os.path.join( controller_name, device_name) + "**************\n" ) #File header   
            basicdeviceslogfile.write(file_content)

        # Closing file
        basicdeviceslogfile.close()

        # Closing reg key
        winreg.CloseKey(key_reg)
        #print ("    *Closing keys registry for other devices")
                    
    except WindowsError:
        print("Error accessing registry")

    if k == 0:
        print("No keys found for basic devices")

    #return info
    return   
   
#------------------------------------------------------------------------------------------------------------------------#
#Print and store the information retrieved from the BLE devices

# BLEKE: BLE Keys Extractor extracts the keys of the BLE devices stored in a Windows machine and saves it 
# into files following the format of the Linux Bluetooth configuration.\n\nJust execute BLEKE.exe to run 
# the program.\n")
# "-i", "--info", help="Shows more info"
# "-n", "--noscreen", help="Stop printing logs on screen"
# "-l", "--log", help="Write logs into a file instead of screen"
# "-f", "--BLEfiles", help="Creates configuration file system for BLE devices in Linux format and BLE devices log"
# "-c", "--classicdeviceslog", help="Write extracted classic devices info and keys into a file"
# "-s", "--script", help="Write the script (.sh) to create the filesystem required to add the BLE devices in Linux"
# Creates one script file to create the files and folders when execute in the bash as per Linux format with the info and keys of the BLE devices paired in this
# in a Windows system.
# Also creates the same files and folders to be copy

###############################################################################################################################
# HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\BTHPORT\Parameters\Keys\e8d0fcda1084
# MasterIRK    REG_BINARY    73651ACC0AC917947F0120C30A7823FC
# 7070aaec1386    REG_BINARY    23FD7FA0F0054FB6A206081D800997F1 Echo Dot-PBT

# HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\BTHPORT\Parameters\Keys\e8d0fcda1084\379a4ba5b3bf Rival 3 Wireless
# HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\BTHPORT\Parameters\Keys\e8d0fcda1084\c9b42148c092 WoMini
# HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\BTHPORT\Parameters\Keys\e8d0fcda1084\dfe5b10bb604 Modern Mobile Mouse
###############################################################################################################################

def bleke(): 
    # Configuration of arguments
    parser = argparse.ArgumentParser("\n\nBLEKE: BLE Keys Extractor extracts the keys of the BLE devices stored in a Windows machine and saves it into files following the format of the Linux Bluetooth configuration.\n\nJust execute BLEKE.exe to run the program. NOTE: System privileges required.\n")
    parser.add_argument("-i", "--info", help="Check privileges and shows more info", action="store_true")
    parser.add_argument("-n", "--noscreen", help="Stop printing logs on screen", action="store_true")
    parser.add_argument("-l", "--log", help="Write logs into a file instead of screen", action="store_true")
    parser.add_argument("-f", "--BLEfiles", help="Creates configuration file system for BLE devices in Linux format and BLE devices log", action="store_true")
    #parser.add_argument("-b", "--BLEdeviceslog", help="Write BLE devices info into a file in Linux format", action="store_true")
    parser.add_argument("-c", "--classicdeviceslog", help="Write extracted classic devices info and keys into a file", action="store_true")
    parser.add_argument("-s", "--script", help="Write the script (.sh) to create the filesystem required to add the BLE devices in Linux", action="store_true")

    args = parser.parse_args()

    #Args options
    if args.info:
        print("Created in 2024 by Francisco Tome.")
        sys.exit() 
    if args.noscreen: #If false cancel the screen print
        f = open(os.devnull, 'w')
        sys.stdout = f
    if args.log:
        print("Creating logfile ")
        logfile = open('logfile.txt','wt')# Redirect standard output to a file  
        sys.stdout = logfile
    if args.BLEfiles:
        if os.path.exists('BLEdevices.txt'): #Reseting file if exists
            os.remove('BLEdevices.txt')
        print("Creating deviceslogfile")
        deviceslogfile = open('BLEdevices.txt', 'a')  #Opens in append mode a file to store every device info for all devices
    
    #Script file creation
    if args.script:
        if os.path.exists('blescript.sh'): #Reseting file if exists
            os.remove('blescript.sh')
        scriptfile = open('blescript.sh', 'a')  #Opens in append mode a file to store the commands for all devices
        scriptfile.write("#! /bin/sh\n")  # First line for bash execution              

    BLE_devices_n = 0 # Total number of devices
    i = 0
    
    #Get computer name in case it could be needed    
    try:
        computername_reg = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
        "SYSTEM\\CurrentControlSet\\Control\\ComputerName\\ComputerName")
        print ("Computer Name (0jO):", winreg.QueryValueEx(computername_reg,'ComputerName')[0])
    except WindowsError:
        Print("Computer name not found")
    try:
        #Opens the Windows registry entry for the BT controller.
        #cmd command: REG QUERY HKLM\SYSTEM\CurrentControlSet\Services\BTHPORT\Parameters\Keys
        controllers_reg = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
        "SYSTEM\\CurrentControlSet\\Services\\BTHPORT\\Parameters\\Keys")

        #Gets and stores the MAC addresses of every available driver in the computer
        for i in range(winreg.QueryInfoKey(controllers_reg)[0]):   #Controllers LOOP     

            controller = winreg.EnumKey(controllers_reg,i) #Obtain the MAC address of the controller
            print ("*************************************************************************************")
            print ("Controller", i+1,":", controller.upper())
            print ("\n*************************************************************************************")
                     
            # Get classic pairing devices
            if (args.classicdeviceslog):
                get_classic_devices(controller)
         
            keys = [] #Contains device keys
            info = [] #Contains device info
            
            #Opens the Windows registry entry for the BLE devices paired (LTK key) with the BT controller.
            #cmd command: REG QUERY HKLM\SYSTEM\CurrentControlSet\Services\BTHPORT\Parameters\Keys\e8d0fcda1084
            devices_reg = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
            "SYSTEM\\CurrentControlSet\\Services\\BTHPORT\\Parameters\\Keys\\" + controller)
            
            #Gets and stores the MAC addresses of every available paired in the computer
            for j in range(winreg.QueryInfoKey(devices_reg)[0]):   #Devices LOOP      
                #try:
                #BLE Devices with LTK
                device = winreg.EnumKey(devices_reg,j)
                print ("*************************************************************************************")
                print ("\n  BLE Paired Devices with LTK:", device.upper(), "(", BLE_devices_n+1, ")")
                print ("")
                
                BLE_devices_n += 1
         
                info = get_info(device) #Get device info
                keys = get_keys(controller, device) #Get device keys
                 
                #Formatting info to be printed and save
                file_path = os.path.join(controller.upper(), device.upper()) #Creates path for controller\device E8D0FCDA1084\582071ABCBED
                #Formating name to be store in the file, unfortunately Windows doesn´t allow file and folders to have a name with ":"
                controller_name =":".join(controller[i:i+2] for i in range(0, len(controller), 2)).upper() #XX:XX:XX:XX:XX Windows doesn´t let saving this name for a folder
                device_name = ":".join(device[i:i+2] for i in range(0, len(device), 2) ).upper()  #XX:XX:XX:XX:XX
                print("\n**************" + os.path.join( controller_name, device_name) + "*******************" )  # Path in Linux
                
                file_content = ("[General]\nName=" + info['Name'] #Content of the device file
                + "\nAppearance=" + info['Appearance']
                + "\nAddressType=" + info['AddressType']
                + "\nSupportedTechnologies=LE;"
                + "\nTrusted=true"
                + "\nBlocked=false"
                + "\nWakeAllowed=true"
                + "\nServices=" + info['Services'] + ";"
                + "\n\n[LongTermKey]\nKey=" + str(keys['LTK'])
                + "\nAuthenticated=0\nEncSize=" + str(keys['KeyLength'])
                + "\nEDiv=" + str(keys['EDIV'])
                + "\nRand=" + str(keys['ERand'])
                + "\n\n[DeviceID]\nSource=2"
                + "\nVendor=" +  str(info['VID'])
                + "\nProduct=" +  str(info['PID'])
                + "\nVersion=" +  str(info['Version']))    
                #If device has more keys theyll be also added to the file
                if 'IRK' in keys:
                    file_content += ("\n\n[IdentityResolvingKey]"
                    + "\nKey=" + str(keys['IRK']))
                if 'CSRKInbound' in keys:
                    file_content += ("\n\n[RemoteSignatureKey]"
                    + "\nKey=" + str(keys['CSRKInbound'])
                    + "\nCounter=0\nAuthenticated=true")
                if 'CSRK' in keys:
                    file_content += ("\n\n[LocalSignatureKey]"
                    + "\nKey=" + str(keys['CSRK'])
                    + "\nCounter=0\nAuthenticated=true")                         
                if 'LTK' and 'CSRKInbound' in keys:
                    file_content += ("\n\n[PeripheralLongTermKey]"
                    + "\nKey=" + str(keys['LTK'])
                    + "\nAuthenticated=3\nEncSize=16\nEDiv=0\nRand=0"
                    + "\n\n[SlaveLongTermKey]"
                    + "\nKey=" + str(keys['LTK'])
                    + "\nAuthenticated=3\nEncSize=16\nEDiv=0\nRand=0"
                    + "\n\n[LinkKey]"
                    + "\nKey=" + winreg.EnumValue(devices_reg,j)[1].hex().upper() #Extracting the LinkKey
                    + "\nType=8\nPINLength=0")                       
               
                print(file_content)
                # Store into devices log file: BLEdevices.txt
                if args.BLEfiles:  #Stores BLE devices info into device log file
                    deviceslogfile.write("\n********************" + os.path.join( controller_name, device_name) + "***************\n" ) #File header   
                    deviceslogfile.write(file_content)
                    #deviceslogfile.write("\n--------------------------------------------------")
                # Store into single files within its right folder: controller/device/file.txt
                if args.BLEfiles:
                    if not os.path.exists(file_path): # If device directory doesn´t exist it'll be created
                        os.makedirs(file_path)                         
                    with open(file_path + "\\info.txt", "wt") as devicefile: #Store the device info into the info file within its folder                      
                        devicefile.write(file_content)               
                    print("-----------Device file created succesfully.-------------")            
                
                # Write the script to create the filesystem required to add the BLE devices in Linux
                if args.script:
                    #command = 'mkdir -p /var/lib/bluetooth/' + controller_name + "/" + device_name + "/" + "; echo -e \"" + file_content + "\" > /var/lib/bluetooth/" + controller_name + "/" + device_name + "/info"
                    command = ("echo \'" + 'mkdir -p /var/lib/bluetooth/' + controller_name + "/" + device_name + "/" 
                    + "; echo -e \"" + file_content 
                    + "\" > /var/lib/bluetooth/" + controller_name + "/" + device_name + "/info" + "\' | bash")
                    #print("Command to run on Linux:\n" + command)
                    scriptfile.write(command)
                    scriptfile.write("\n#################################################################\n")
               
            #Closing device key
            winreg.CloseKey(devices_reg)
            #print (" *Closing device registry", devices_reg)
    
        winreg.CloseKey(controllers_reg) #Closes the registry key
        #print ("*Closing controller registry", devices_reg)             
        
    except WindowsError:
        print("Error accessing registry")
    if controller == "":
        print("No BT controller available in this computer.")
    if BLE_devices_n == 0:
        print("No Bluetooth paired devices available in this computer.")

    # Close the log files
    if args.BLEfiles:
        deviceslogfile.close()       
    if args.log:
        logfile.close() 
    if args.noscreen: #If false cancel the screen print
        f.close()       
    if args.script: #If false cancel the screen print
        scriptfile.close()       
    sys.exit()

#------------------------------------------------------------------------------------------------------------------------#

if __name__ == "__main__":
    check_privileges()
    bleke()
    
   
    