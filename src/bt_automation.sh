#!/usr/bin/expect -f


spawn bluetoothctl -a
sleep 2
send "scan on\r"
sleep 2
send "agent on\r"
sleep 2
send "discoverable on\r"
sleep 2
send "pairable on\r"
sleep 5
send "quit\r"
expect eof
