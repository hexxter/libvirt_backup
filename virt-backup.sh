#!/bin/bash
cd /home/alex/python_backup
source bin/activate

MAILTO=alexander.kratzer@semsotec.de

(
echo Backups from container.garching.semsotec.de
echo -------------------------------------------
echo -n Date:
date

if [ -f /mnt/bak/STORAGE ]
then
	echo do Bakup...
	echo -------------------------------------------
	echo 1. SAGE VM
	bin/python virt-backup.py SAGE SAGE_vm.img /mnt/bak/SAGE
	echo -------------------------------------------
	echo 2. redmine VM
	bin/python virt-backup.py redmine redmine.img /mnt/bak/redmine
	echo -------------------------------------------
	echo
	echo All done!
	echo -n Date:
	date
else
	echo backup volume not mounted
fi
) 2>&1 | mail -s backup $MAILTO
