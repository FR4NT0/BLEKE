Print and store the information retrieved from the BLE devices

BLEKE: BLE Keys Extractor extracts the keys of the BLE devices stored in a Windows machine and saves it 


into files following the format of the Linux Bluetooth configuration.\n\nJust execute BLEKE.exe to run 

the program.\n")
"-i", "--info", help="Shows more info"
"-n", "--noscreen", help="Stop printing logs on screen"
"-l", "--log", help="Write logs into a file instead of screen"
"-f", "--BLEfiles", help="Creates configuration file system for BLE devices in Linux format and BLE devices log"
"-c", "--classicdeviceslog", help="Write extracted classic devices info and keys into a file"
"-s", "--script", help="Write the script (.sh) to create the filesystem required to add the BLE devices in Linux"
Creates one script file to create the files and folders when execute in the bash as per Linux format with the info 
and keys of the BLE devices paired in this in a Windows system.
