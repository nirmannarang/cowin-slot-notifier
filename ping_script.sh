#!/bin/bash
flagger=0
count=0
while true
do
	if pidof -x "vaccine_spotter.py" >/dev/null; then
    		echo "Process already running"
		if [ $flagger -eq 0 ]
		then
			telegram-send "Resolved: AWS Vaccine Spotter is up now."
			flagger=1
			count=0
		fi
    	else
    		echo "!!!!Urgent!!!!  AWS Vaccine Spotter is down."
    		telegram-send "!i!i!i! Urgent !i!i!i!  AWS Vaccine Spotter is down."
		flagger=0
		count=$((count + 1))
	fi

	if [ $count -gt 2 ]
	then
		nohup ./vaccine_spotter.py &
	fi
	sleep 20
	sudo free -mh && sudo sync && sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches' && sudo free -mh
done
