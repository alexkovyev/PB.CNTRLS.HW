while true; do
	echo "sync started"
	sshpass -p "orangepi" rsync -uav --progress --exclude "*.avi" --exclude "*.mp4"  /home/prostoichelovek/projects/dispenser_main orangepi@192.168.1.69:/home/orangepi/PB.CNTRLS.HW;
	echo "synced"
	sleep 5;
done
