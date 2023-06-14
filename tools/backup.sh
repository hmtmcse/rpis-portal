#!/bin/bash

cd /home/v-host/kpir.banglafighter.com/ins-reunion
DATE_TIME=`date +%d-%m-%Y_%H-%M-%S`
echo $DATE_TIME
cp pweb.sqlite3 "/opt/kpir-2023/$DATE_TIME.sqlite3"
cd /opt/kpir-2023/
git add --all
git commit -m "Backup at $DATE_TIME"
git push --all