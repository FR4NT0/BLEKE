#! /bin/sh
echo 'mkdir -p /var/lib/bluetooth/E8:D0:FC:DA:10:84/58:20:71:AB:CB:ED/; echo -e "[General]
Name=Galaxy A14 5G
Appearance=0x0
AddressType=public
SupportedTechnologies=LE;
Trusted=true
Blocked=false
WakeAllowed=true
Services=00001800-0000-1000-8000-00805f9b34fb;00001801-0000-1000-8000-00805f9b34fb;

[LongTermKey]
Key=66AEE0B96C703405F9B25FC9967A7712
Authenticated=0
EncSize=16
EDiv=0
Rand=0

[DeviceID]
Source=2
Vendor=117
Product=256
Version=0

[IdentityResolvingKey]
Key=718D197008A16DFA036D0EF53DAFFBB8

[RemoteSignatureKey]
Key=F1D46B02DB91BFE54142C42E8D974DB0
Counter=0
Authenticated=true

[LocalSignatureKey]
Key=5AC07051A2614197A9185E3EE7BB30E7
Counter=0
Authenticated=true

[PeripheralLongTermKey]
Key=66AEE0B96C703405F9B25FC9967A7712
Authenticated=3
EncSize=16
EDiv=0
Rand=0

[SlaveLongTermKey]
Key=66AEE0B96C703405F9B25FC9967A7712
Authenticated=3
EncSize=16
EDiv=0
Rand=0

[LinkKey]
Key=B95326D9FEB58AA2FF17BAF8A476C2ED
Type=8
PINLength=0" > /var/lib/bluetooth/E8:D0:FC:DA:10:84/58:20:71:AB:CB:ED/info' | bash
#################################################################
echo 'mkdir -p /var/lib/bluetooth/E8:D0:FC:DA:10:84/DF:E5:B1:0D:B6:04/; echo -e "[General]
Name=Modern Mobile Mouse
Appearance=0x3c2
AddressType=static
SupportedTechnologies=LE;
Trusted=true
Blocked=false
WakeAllowed=true
Services=00001800-0000-1000-8000-00805f9b34fb;00001801-0000-1000-8000-00805f9b34fb;0000180a-0000-1000-8000-00805f9b34fb;0000180f-0000-1000-8000-00805f9b34fb;00001812-0000-1000-8000-00805f9b34fb;

[LongTermKey]
Key=F926C59DB656EA73410A95C4229AD33F
Authenticated=0
EncSize=16
EDiv=52789
Rand=7552872943690607367

[DeviceID]
Source=2
Vendor=1118
Product=2087
Version=259" > /var/lib/bluetooth/E8:D0:FC:DA:10:84/DF:E5:B1:0D:B6:04/info' | bash
#################################################################
