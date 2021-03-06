# Websense/Forcepoint WCG Auto Backup Script
This is a script that was designed to run on Websense/Forcepoint appliances to create automatic backups of the WCG settings "WCG Snapshot" and FTP them to an FTP Server. Currently the script creates a tar.gz file of the backup to upload, in the future it will be changed to create the same directory structure that the proxy does for easier remote restores.

Recently there was a custom log added which can be viewed in the WCG UI. The log can be accessed via Configure > Logs > System and then select "snapshot_script.log" from the dropdown box. An example of the log:

``` 2016-04-25:07:41:29 - Backup wcghostname.tar.gz was created and transfered to the FTP Server! MD5 of file is: 760ec68b1203eebc7b1579f7965d2a67 ```

This script is provided without any warranty or support. Any issues feel free to post them here on Github so I can look at them.


###Installation:
To install run the following commands on the WCG Dom or OS where the proxy is installed:
```
wget -O config.ini https://pastebin.com/raw/kQjzRA9U --no-check-certificate
wget -O forcepoint_auto_backup.py https://pastebin.com/raw/KgSrmAVQ --no-check-certificate
chmod +x forcepoint_auto_backup.py
(crontab -l 2>/dev/null; echo "00 00 * * * python /root/forcepoint_auto_backup.py") | crontab -
```

To manually run the script:
```# python forcepoint_auto_backup.py```

#####SCP Setup:
To use SCP you need to setup your keys ahead of time. To generate a new set of private keys on the Content Gateway machine the following command and follow the prompts, do not set a password or the script will fail:

```root@proxy# ssh-keygen -t rsa```

Then you need to export the key to your SCP server:

```root@proxy# ssh-copy-id user@server```

Once this is done you need to enable SCP in the config.ini by changing the value to "True"


###Planned Changes:
- Change from tar.gz to exact directory structure WCG uses for easy remote restores.
- (COMPLETED) Move the configuration values to a .ini file for easy setup.
- (COMPLETED) Migrate from bash to Python for the script.
- Create an installer.
- (Completed) Add SCP support with SSH keys for better security.


*Notes: This script was tested working and developed on a Websense/Forcepoint V1000G3 running version 8.0.1
