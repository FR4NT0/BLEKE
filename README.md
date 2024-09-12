Welcome to the BLEKE project.

This project was developed as part of an investigation to find out if it was possible to extract BLE pairing keys from a Windows device and impersonate it from a Linux device against those paired devices.

BLEKE BLE Keys extractor simplifies the extraction of the pairing information from Windows registry and converts it into Linux Ubunty Bluetooth configuration files format.
Print and store the information retrieved from the BLE devices

BLEKE options
default option print the information of paired BLE devices on the screen
"-i", "--info": Shows more info
"-n", "--noscreen": Stop printing logs on screen
"-l", "--log": Write extracting activity logs into a file instead of screen
"-f", "--BLEfiles": Creates configuration file system (controller folder, device folder and "info" file) for BLE devices in Linux format and BLE devices log. Note Windows folder and files can´t contain ":" son it must be added when placed in var/lib/bluetooth.
"-c", "--classicdeviceslog": Write extracted classic devices info and keys into a file
"-s", "--script": Write the script (.sh) to create the filesystem (controller folder, device folder and "info" file) required to add the BLE devices in Linux.

