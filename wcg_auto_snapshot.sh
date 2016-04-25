#!/bin/bash
#=========================================================================================
#title               :wcg_auto_snapshot.sh
#description         :This script is called by a cron job to take snapshot and FTP them.
#author		         :Alan Matson (alan.matson@insight.com)
#date                :2016-04-20
#version             :0.91    
#notes               :script is called via crontab "00 00 * * * bash /root/wcg_auto_snapshot.sh"
#websense_version    :8.0.1 (Running CentOS 6.3 Kernel 3.6.3)
#license             :GPLv3
#changelog           :https://github.com/ajmatson/Websense-WCG-Auto-Backup-Script/blob/master/CHANGELOG
#=========================================================================================

#Change the values for your FTP Server and local directory
ftpserverip="1.1.1.1"
username="USERNAME"
password="PASSWORD"
remotedir="/WebsenseBackups/WCG"
localdir="/opt/WCG/config/snapshots/$fhostname"

###################################################################################################
## DO NOT MODIFY BELOW THIS LINE OR THE SCRIPT MAY BECOME UNUSABLE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ##
###################################################################################################


#Set the variables stock:
curdate=`date +%Y%m%d`
host="$HOSTNAME"
host2=${host%-*}
fhostname=$host2$curdate
logfile="/opt/WCG/logs/snapshot_script.log"


#Create the log file is it does not exist already:
if [ ! -e "$logfile" ] ; then
    touch "$logfile"
fi

#Run the snapshot to the /opt/WCG/config/snapshots directory
echo "Running snapshot!"
/opt/WCG/bin/content_line -N $fhostname
echo $fhostname

#Zip up the directory for transfer:
cd $localdir
tar -czvf /tmp/$fhostname.tar.gz -C /opt/WCG/config/snapshots/$fhostname .

#Login to FTP and transfer the gzip file:
ftplog="/tmp/ftptmplog"
ftp -inv $ftpserverip <<EOF > $ftplog 
user $username $password
lcd /tmp/
cd $remotedir
put $fhostname.tar.gz
quit
exit;
EOF

#Cleanup temporary files and write the success/failure to the custom log
ftpsuccess="226 Transfer complete"
if fgrep "$ftpsuccess" $ftplog ;then
   logdate=`date +%Y-%m-%d:%H:%M:%S`
   echo "$logdate - Backup $fhostname.tar.gz was created and transfered to the BlueOx FTP Server!" >> $logfile
   rm -rf /opt/WCG/config/snapshots/$fhostname
   rm -rf /tmp/$fhostname.tar.gz
   rm -rf /tmp/ftptmplog
else
   logdate=`date +%Y-%m-%d:%H:%M:%S`
   echo "$logdate - Backup $fhostname.tar.gz failed, please investiagate!" >> $logfile
   rm -rf /opt/WCG/config/snapshots/$fhostname
   rm -rf /tmp/$fhostname.tar.gz
   rm -rf /tmp/ftptmplog
fi
exit 0
