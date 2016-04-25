# Websense-WCG-Auto-Backup-Script
This is a script that was designed to run on Websnse appliances to create automatic backups of the WCG settings "WCG Snapshot" and FTP them to an FTP Server. Currently the script creates a tar.gz file of the backup to upload, in the future it will be changed to create the same directory structure that the proxy does for easier remote restores.

This script is provided without any warranty or support. Any issues feel free to post them here on Github so I can look at them.

#Planned Changes:
- Add MD5 sum to the custom log for verification that FTP server is receiving correctly
- Change from tar.gz to exact directory structure WCG uses for easy remote restores.
