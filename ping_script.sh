#!/bin/bash
flagger=0
count=0
chmod +x cowin_notifier.py
while true
do
	if pidof -x "cowin_notifier.py" >/dev/null; then
    		echo "Process already running"
		if [ $flagger -eq 0 ]
		then
			telegram-send "Resolved: AWS Slot Notifier is up now."
			flagger=1
			count=0
		fi
    	else
    		echo "!!!!Urgent!!!!  AWS Slot Notifier is down."
    		telegram-send "!i!i!i! Urgent !i!i!i!  AWS Slot Notifier is down."
		flagger=0
		count=$((count + 1))
	fi

	if [ $count -gt 2 ]
	then
		nohup ./cowin_notifier.py &
	fi
	sleep 20
	sudo sync && sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
done
