# Websense WCG Auto Backup Script
This is a script that was designed to run on Websnse appliances to create automatic backups of the WCG settings "WCG Snapshot" and FTP them to an FTP Server. Currently the script creates a tar.gz file of the backup to upload, in the future it will be changed to create the same directory structure that the proxy does for easier remote restores.

Recently there was a custom log added which can be viewed in the WCG UI. The log can be accessed via Configure > Logs > System and then select "snapshot_script.log" from the dropdown box. An example of the log:

2016-04-25:07:41:29 - Backup wcghostname.tar.gz was created and transfered to the FTP Server! MD5 of file is: 760ec68b1203eebc7b1579f7965d2a67




This script is provided without any warranty or support. Any issues feel free to post them here on Github so I can look at them.

#Planned Changes:
- Change from tar.gz to exact directory structure WCG uses for easy remote restores.
