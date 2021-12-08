import os
import sys
import time
import keyboard

def sendPing(interfaceName, repeat):
    print('Start Ping...')

    # Get Gateway IP
    gwipcmd = "ip route | grep -w 'default via.*dev " + interfaceName + "' | awk '{print $3}'"
    gwip = os.popen(gwipcmd).read()

    # Send Ping
    while True:
        # Request 5 Times, Ping from specified NIC to gateway
        pingcmd = 'ping -q -c ' + repeat + ' -I ' + interfaceName + ' ' + gwip + ' 1> /dev/null'
        os.system(pingcmd)


        # if Pressed Q, Exit
        if keyboard.read_key() == "q":
            break

        # Sleep
        time.sleep(1)

if __name__ == '__main__':
    # python3 only_ping.py wlan0 5
    # wlan0 - Send Ping Interface
    # 5 - number of repetitions

    pingInterface = sys.argv[1]
    repeat = sys.argv[2]
    sendPing(pingInterface, repeat)
