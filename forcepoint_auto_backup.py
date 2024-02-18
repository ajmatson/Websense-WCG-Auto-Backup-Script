#!/usr/bin/env python
__author__ = "Alan Matson"
__copyright__ = "Copyright 2016, Alan Matson"
__license__ = "GPLv3"
__version__ = "0.93a"
__maintainer__ = "Alan Matson"
__email__ = "alan (at) gmail (dot) com"
__status__ = "Development"

###########################################################################################################
## Development Note: SCP is not currently functionioning. Please refrain from using until future update. ##
##                                                                                                       ##
## Also due to bug in Forcepoint command line backup several additional files manually added.            ##
###########################################################################################################


import socket, os, subprocess, tarfile, hashlib, time
from ftplib import FTP
from datetime import datetime
from ConfigParser import SafeConfigParser
from distutils.dir_util import copy_tree
from shutil import copyfile

# Import variables from config.ini and set a few others:
global server
global uname
global passw
global remoted
global locald
global currdate
global hostname
global fhostname
global logfile
global logdate
global scpstat
config = SafeConfigParser()
config.read("config.ini")
scpstat = config.get('Configuration', 'scpenable')
server = config.get('Configuration', 'serverip')
uname = config.get('Configuration', 'username')
passw = config.get('Configuration', 'password')
remoted = config.get('Configuration', 'remotedir')
locald = config.get('Configuration', 'localdir')
currdate = datetime.now().strftime('%Y%m%d')
hostname = socket.gethostname()
hostname = hostname.split("-", 1)[0]
hostname = hostname.split(".", 1)[0]
fhostname = hostname + currdate
logfile = "/opt/WCG/logs/snapshot_script.log"
logdate = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def snapshot():
    #Run the snapshot on the appliance:
    #print "Running snapshot!"
    shellcmd = "/opt/WCG/bin/content_line -N %s" % fhostname
    subprocess.Popen(shellcmd, shell=True)
    dirname = "/opt/WCG/config/snapshots/" + fhostname
    time.sleep(10)
    os.mkdir(dirname + '/ddscomm', 0777)
    os.mkdir(dirname + '/ant_server', 0777)
    copy_tree('/opt/WCG/config/ddscomm/', dirname + '/ddscomm')
    copy_tree('/opt/WCG/config/ant_server/', dirname + '/ant_server')
    copyfile('/opt/WCG/bin/websense.ini', dirname + '/websense.ini')
    copyfile('/opt/WCG/config/broker.config', dirname + '/broker.config')


def tarfiles():
    #Tar the files into one compressed file:
    global tarname
    global dirname
    tarname = "/tmp/" + fhostname + ".tar.gz"
    dirname = "/opt/WCG/config/snapshots/" + fhostname
    tar = tarfile.open(tarname, 'w:gz')
    tar.add(dirname)
    tar.close()


def ftpfiles():
    #Time to FTP the file to the server:
    filen = fhostname + ".tar.gz"
    ftp = FTP(server)
    ftp.login(uname,passw)
    ftp.cwd(remoted)
    with open('/tmp/%s' % filen, 'r') as filename:
        ftpresponse = ftp.storbinary('STOR %s' % filen, filename)
    ftp.quit()

    #Check the FTP response
    if "226 Successfully transferred" not in ftpresponse:
        with open(logfile, 'a') as logf:
            logf.write("%s - Backup %s failed, please investigate! \n" % (logdate, filen))
    else:
        md5filen = "/tmp/" + filen
        md5sum = hashlib.md5(open(md5filen, 'rb').read()).hexdigest()
        with open(logfile, 'a') as logf:
            logf.write("%s - Backup %s was created and transfered to the FTP Server! MD5 of file is: %s \n" % (logdate, filen, md5sum))
    os.remove(tarname)


def scpfiles():
    filen = fhostname + ".tar.gz"
    localfile = '/tmp/' + filen
    remotefile = '/tmp/' + filen
    command = 'scp "%s" "%s@%s:%s" % (localfile, uname, server, remotefile)'
    scpresponse = subprocess.Popen(command, shell=True)
    print scpresponse
    if "is done" not in scpresponse:
        with open(logfile, 'a') as logf:
            logf.write("%s - Backup %s failed, please investigate! \n" % (logdate, filen))
    else:
        md5filen = "/tmp/" + filen
        md5sum = hashlib.md5(open(md5filen, 'rb').read()).hexdigest()
        with open(logfile, 'a') as logf:
            logf.write("%s - Backup %s was created and transfered to the FTP Server! MD5 of file is: %s \n" % (
            logdate, filen, md5sum))
    os.remove(tarname)

def main():
    snapshot()
    time.sleep(2)
    tarfiles()
    time.sleep(2)
    #if scpstat is "True" or "true":
    #    scpfiles()
    #else:
    #    ftpfiles()
    ftpfiles()

if __name__ == "__main__":
    main()
