#!/bin/bash
wget -q --spider http://google.com
if [ $? -eq 0 ]; then
	echo "online"
else
	echo "offline, need internets to setup"
	exit 1
fi

echo "######################"
echo "Updating Distribution"
echo "######################"
sudo apt-get update && sudo apt-get upgrade
# vim is a nice editor, 
sudo apt-get install -y vim ffmpeg exfat-fuse

echo "###############################"
echo "Adding auto-mounting of sd_card"
echo "###############################"
if [ -e /dev/sda1 ]; then
	echo "" >> /dev/null
else
	echo "#### SD card Missing!!! Wait... it shouldn't be"
	exit 3
fi
mkdir /media/sd_card
sudo echo "/dev/sda1	/media/sd_card	exfat	user,fmask=0111,dmask=0000,nofail	0	0" >> /etc/fstab

sudo mount /dev/sda1 /media/sd_card
if [ $? -eq 0 ]; then
	echo "#### SD card automount add successful"
else
	echo "#### Failed to add sd card automount"
	exit 2
fi

echo "######################"
echo "Add participant user"
echo "######################"
mkdir /home/participant
sudo useradd -u 1001 -g "users" -d /home/participant -s /bin/bash -p $(echo 12345 | openssl passwd -1 -stdin) participant

if [ $? -eq 0 ]; then
	echo "#### User add successful"
else
	echo "#### Failed to add user"
	exit 2
fi

echo "##########################"
echo "Add autostart for chromium"
echo "##########################"

touch /home/participant/.config/autostart/chromium.desktop
chown participant:participant /home/participant/.config/autostart/chromium.desktop
chmod 664 /home/participant/.config/autostart/chromium.desktop
echo "[Desktop Entry]
Encoding=UTF-8
Version=0.9.4
Type=Application
Name=Chromium
Comment=Autostart Chromium Browser
Exec=/home/participant/.config/autostart/forever_chromium.sh
OnlyShowIn=XFCE;
StartupNotify=false
Terminal=false
Hidden=false" > /home/participant/.config/autostart/chromium.desktop


echo "sed -i 's/\"exited_cleanly\": false/\"exited_cleanly\": true' /home/participant/.config/chromium/Default/Preferences" > /home/participant/.config/autostart/forever_chromium.sh
echo "while true; do chromium-browser --noerrdialogs --kiosk 127.0.0.1 --incognito; sleep 1s; done" > /home/participant/.config/autostart/forever_chromium.sh
chown participant:participant /home/participant/.config/autostart/forever_chromium.sh
chmod 755 /home/participant/.config/autostart/forever_chromium.sh

echo "############################"
echo "Add autostart for vlc telnet"
echo "############################"

touch /home/participant/.config/autostart/vlc.desktop
chown participant:participant /home/participant/.config/autostart/vlc.desktop
chmod 664 /home/participant/.config/autostart/vlc.desktop
echo "[Desktop Entry]
Encoding=UTF-8
Version=0.9.4
Type=Application
Name=vlc
Comment=Autostart vlc with telnet remote control
Exec=vlc -I telnet --telnet-password=test
OnlyShowIn=XFCE;
StartupNotify=false
Terminal=false
Hidden=false" > /home/participant/.config/autostart/vlc.desktop

echo "#########################"
echo "vimrc. because, important"
echo "#########################"
touch /home/participant/.vimrc
chown participant:participant /home/participant/.vimrc
chmod 664 /home/participant/.vimrc
echo "set tabstop=4" >> /home/participant/.vimrc
echo "set expandtab" >> /home/participant/.vimrc
echo "set number" >> /home/participant/.vimrc

echo "######################"
echo "Done!"
echo "######################"

