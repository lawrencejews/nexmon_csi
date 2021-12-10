## Nexmon Lab Set-Up
### Preparing the Raspberry-pi
- Check the kernel version -> uname -r
- Move to root -> sudo su
- Add kernel headers: apt install git libgmp3-dev gawk qpdf bison flex make autoconf libtool texinfo raspberrypi-kernel-headers
- Clone Repo: git clone https://github.com/seemoo-lab/nexmon.git
- Configure 5.10-y from 5.4-y
### Compiling the additional libraries
- cd /home/pi/nexmon/buildtools/isl-0.10
- ./configure && make && make install
- Create a link to lib: ln -s /usr/local/lib/libisl.so /usr/lib/arm-linux-gnueabihf/libisl.so.10
- cd /home/pi/nexmon/buildtools/mpfr-3.1.4
- Prepare Makefile: autoreconf -f -i
- ./configure && make && make install
- Create link to the lib: ln -s /usr/local/lib/libmpfr.so /usr/lib/arm-linux-gnueabihf/libmpfr.so.4
### Install Nexmon patches
- cd /home/pi/nexmon
- source setup_env.sh
- make
- cd /home/pi/nexmon/patches/bcm43455c0/7_45_189/nexmon/
- make
- make backup-firmware
- make install-firmware
- cd /home/pi/nexmon/utilities/nexutil
- make && make install
### Load Modified Driver after reboot
- Run to find the: PATH modinfo brcmfmac
- Move location: mv /lib/modules//5.10.63-v7l+/kernel/drivers/net/wireless/broadcom/brcm80211/brcmfmac/brcmfmac.ko /lib/modules//5.10.63-v7l+/kernel/drivers/net/wireless/broadcom/brcm80211/brcmfmac/brcmfmac.ko.orig
- Copy: cp /home/Desktop/CSI/nexmon/patches/bcm43455c0/7_45_189/nexmon/brcmfmac_5.10.y-nexmon/brcmfmac.ko /lib/modules//5.10.63-v7l+/kernel/drivers/net/wireless/broadcom/brcm80211/brcmfmac/
- Reload all kernel modules: depmod -a
- Reboot
- Then check the physical id of wlan0: iw dev
- iw phy0 info
## Nexmon_CSI
- cd /home/pi/nexmon/patches/bcm43455c0/7_45_189/
- Inside nexmon clone: git clone https://github.com/lawrencejews/nexmon_csi.git
- cd nexmon_csi
- make install-firmware
### Install before CSI-Extraction
- sudo apt update && sudo apt install libpcap-dev python3-pypcap 
- sudo pip3 install numpy --upgrade
- sudo pip3 install dpkt pandas keyboard
### Extractor
- These are CSI extraction files
- nexutil -k
- ./makecsiparams - c [channel] -C 1 -N 1 -m [Mac Address(ping)]
- ./makecsiparams -c 7 -C 1 -N 1 -m 1C:91:80:F1:EE:AF 
- pkill wpa_supplicant
- ifconfig wlan0 up
- nexutil -I wlan0 -s 500 -b -l 34 -v [makecsiparams result]
- nexutil -I wlan0 -s 500 -b -l 34 -v BxABEQAAAQAckYDx7q8AAAAAAAAAAAAAAAAAAAAAAAAAAA==
- iw phy `iw dev wlan0 info | gawk '/wiphy/ {printf "phy" $2}'` interface add mon0 type monitor && ifconfig mon0 up
- python3 only_sniffing.py wlan0
NOTE: 
- You should run on the same network for wireless extraction from the sender PC to receiver PC.
- Make sure your autoconf -> 2.69 & automake-1.15
- wget https://ftp.gnu.org/gnu/automake/automake/automake-1.15.tar.gz 
- wget https://ftp.gnu.org/gnu/autoconf/autoconf/autoconf-2.71.tar.gz
- Extract -> tar -xzvf [PACKAGES]
- Change to folder and Build & install -> ./configure && make && make install
