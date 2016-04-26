#!/usr/bin/env python
__author__ = "Alan Matson"
__copyright__ = "Copyright 2016, EchoTEK Solutions"
__license__ = "GPLv3"
__version__ = "0.93"
__maintainer__ = "Alan Matson"
__email__ = "alan (at) echotek (dot) us"
__status__ = "Development"

import socket, os, subprocess, tarfile, hashlib
from ftplib import FTP
from datetime import datetime
from ConfigParser import SafeConfigParser

# Import variables from config.ini and set a few others:
config = SafeConfigParser()
config.read("config.ini")
server = config.get('Configuration', 'ftpserverip')
uname = config.get('Configuration', 'username')
passw = config.get('Configuration', 'password')
remotd = config.get('Configuration', 'remotedir')
locald = config.get('Configuration', 'localdir')
currdate = datetime.now().strftime('%Y%m%d')
hostname = socket.gethostname()
hostname = hostname.split("-", 1)[0]
fhostname = hostname + currdate
logfile = "/opt/WCG/logs/snapshot_script.log"
logdate = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

#Run the snapshot on the appliance:
print "Running snapshot!"
shellcmd = "/opt/WCG/bin/content_line -N %s" % fhostname
subprocess.Popen(shellcmd, shell=True)

#Tar the files into one compressed file:
tarname = "/tmp/" + fhostname + ".tar.gz" 
dirname = "/opt/WCG/config/snapshots/" + fhostname
tar = tarfile.open(tarname, 'w:gz')
tar.add(dirname)
tar.close()

#Time to FTP the file to the server:
filen = fhostname + ".tar.gz"
ftp = FTP(server)
ftp.login(uname,passw)
with open('/tmp/%s' % filen, 'r') as filename:
    ftpresponse = ftp.storbinary('STOR %s' % filen, filename)
ftp.quit()


#Check the FTP response
print ftpresponse
if "226 Successfully transferred" not in ftpresponse:
    with open(logfile, 'a') as logf:
        logf.write("%s - Backup $s failed, please investigate!" % (logdate, filen))
else:
    md5filen = "/tmp/" + filen
    md5sum = hashlib.md5(open(md5filen, 'rb').read()).hexdigest()
    with open(logfile, 'a') as logf:
        logf.write("%s - Backup %s was created and transfered to the FTP Server! MD5 of file is: %s" % (logdate, filen, md5sum))
