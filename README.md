Welcome to the BLEKE project.

This project was developed as part of an investigation to find out if it was possible to extract paired BLE devices information from a Windows device and gain access to them from an unrelated Linux device.

BLEKE BLE Keys extractor simplifies the extraction of the pairing information from Windows registry and converts it into Linux Ubuntu Bluetooth configuration files format.
Print and store the information retrieved from the paired BLE devices

NOTE: SYSTEM privileges required.

BLEKE options
default option print the information of paired BLE devices on the screen
"-i", "--info": Shows more info.

"-n", "--noscreen": Stop printing logs on screen.

"-l", "--log": Write extracting activity logs into a file instead of screen.

"-f", "--BLEfiles": Creates configuration file system (controller folder, device folder and "info" file) for BLE devices in Linux format and BLE devices log. Note Windows folders and files can´t contain character ":" so it must be added when placed in Linux path: var/lib/bluetooth.

"-c", "--classicdeviceslog": Write extracted classic devices info and keys into a file.

"-s", "--script": Write the script (.sh) to create the filesystem (controller folder, device folder and "info" file) required to add the BLE devices in Linux. NOTE: This bash script needs to be converted to Unix format before executing so it needs to run "sed -i 's/\r$//' BLEscript.sh” to convert the line endings.

Files examples are included in the project.

