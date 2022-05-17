# Setting up system service files
for s in update_dashboard; do
	sudo cp ~/bleed-orange-measure-iaq/services/${s}.service /lib/systemd/system/${s}.service
 	sudo systemctl enable ${s}
    sudo systemctl start ${s}
done