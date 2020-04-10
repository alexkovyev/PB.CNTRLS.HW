while true; do
	sshpass -p "orangepi" rsync -uav --delete /home/prostoichelovek/MEGA/dispenser orangepi@192.168.1.65:/home/orangepi/dispenser_new;
	sleep 5;
done
