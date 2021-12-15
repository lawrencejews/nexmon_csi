# Nexmon Lab Set-Up 
#### NOTE: Remember your clone location for file configurations. 
### Preparing the Raspberry-pi
1. Check the kernel version -> uname -r
2. Move to root -> sudo su
3. Add kernel headers: ``` apt install git libgmp3-dev gawk qpdf bison flex make autoconf libtool texinfo raspberrypi-kernel-headers ```
4. Clone Repo: `git clone https://github.com/seemoo-lab/nexmon.git`
5. Configure 5.10-y from 5.4-y
## Compiling the additional libraries
1. cd /home/pi/nexmon/buildtools/isl-0.10
2. ./configure && make && make install
3. Create a link to lib: ``` ln -s /usr/local/lib/libisl.so /usr/lib/arm-linux-gnueabihf/libisl.so.10 ```
4. cd /home/pi/nexmon/buildtools/mpfr-3.1.4
5. Prepare Makefile: autoreconf -f -i
6. ./configure && make && make install
7. Create link to the lib: ``` ln -s /usr/local/lib/libmpfr.so /usr/lib/arm-linux-gnueabihf/libmpfr.so.4 ```
## Install Nexmon patches
1. cd /home/pi/nexmon
2. source setup_env.sh
3. make
4. cd /home/pi/nexmon/patches/bcm43455c0/7_45_189/nexmon/
5. make
6. make backup-firmware
7. make install-firmware
8. cd /home/pi/nexmon/utilities/nexutil
9. make && make install
## Load Modified Driver after reboot
1. Run to find the: PATH modinfo brcmfmac
2. Move location: ``` mv /lib/modules//5.10.63-v7l+/kernel/drivers/net/wireless/broadcom/brcm80211/brcmfmac/brcmfmac.ko /lib/modules//5.10.63-v7l+/kernel/drivers/net/wireless/broadcom/brcm80211/brcmfmac/brcmfmac.ko.orig ```
3. Copy: ``` cp /home/Desktop/CSI/nexmon/patches/bcm43455c0/7_45_189/nexmon/brcmfmac_5.10.y-nexmon/brcmfmac.ko /lib/modules//5.10.63-v7l+/kernel/drivers/net/wireless/broadcom/brcm80211/brcmfmac/ ```
4. Reload all kernel modules: depmod -a
5. Reboot
6 Then check the physical id of wlan0: iw dev
7 iw phy0 info
# Nexmon_CSI
1. cd /home/pi/nexmon/patches/bcm43455c0/7_45_189/
2. Inside nexmon clone: `git clone https://github.com/lawrencejews/nexmon_csi.git`
3. cd nexmon_csi
4. make install-firmware
## Install before CSI-Extraction
1. sudo apt update && sudo apt install libpcap-dev python3-pypcap 
2. sudo pip3 install numpy --upgrade
3. sudo pip3 install dpkt pandas keyboard
## Extractor: These are CSI extraction files && install
### Run sniffing .py file in a different terminal after configuration.
1. cd nexmon
2. run: source setup_env.sh
3. cd /home/pi/Desktop/CSI/nexmon/patches/bcm43455c0/7_45_189/nexmon_csi
4. make install-firmware
5. cd /home/pi/Desktop/CSI/nexmon/patches/bcm43455c0/7_45_189/nexmon_csi/utils/makecsiparams
6. nexutil -k
7. ./makecsiparams - c [channel] -C 1 -N 1 -m [Mac Address(ping)]
8. ./makecsiparams -c 7 -C 1 -N 1 -m 1C:91:80:F1:EE:AF 
9. pkill wpa_supplicant
10. ifconfig wlan0 up
11. nexutil -I wlan0 -s 500 -b -l 34 -v [makecsiparams result]
12. nexutil -I wlan0 -s 500 -b -l 34 -v BxABEQAAAQAckYDx7q8AAAAAAAAAAAAAAAAAAAAAAAAAAA==
13. iw phy `iw dev wlan0 info | gawk '/wiphy/ {printf "phy" $2}'` interface add mon0 type monitor && ifconfig mon0 up
14. sudo apt install tcpdump
15. Run in a different terminal for .csv`python3 only_sniffing.py wlan0` OR Run `tcpdump -i wlan0 dst port 5500` for .pcap file
## NOTE: 
1. You should run on the same network for wireless extraction from the sender PC to receiver PC.
2. Make sure your autoconf -> 2.69 & automake-1.15
3. `wget https://ftp.gnu.org/gnu/automake/automake/automake-1.15.tar.gz `
4. `wget https://ftp.gnu.org/gnu/autoconf/autoconf/autoconf-2.71.tar.gz`
5. Extract -> tar -xzvf [PACKAGES]
6. Change to folder and Build & install -> ./configure && make && make install
