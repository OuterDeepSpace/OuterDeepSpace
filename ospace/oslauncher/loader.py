#!/usr/bin/python -t

"""
Synchronize and run sources
"""
import sys
import os
from urlgrabber.grabber import URLGrabber
from ConfigParser import SafeConfigParser
from StringIO import StringIO
from urlparse import urlparse

def log(*args):
    for arg in args:
        sys.stdout.write(str(arg))
        sys.stdout.write(" ")
    sys.stdout.write("\n")
    sys.stdout.flush()

def getBaseDir(baseUrl):
    location, path = urlparse(baseUrl)[1:3]
    location = location.replace(":", "_")
    path = path.replace("/", "_")
    return os.path.abspath(os.path.join(os.path.expanduser("~"), ".netstart", location + path))

def isUpToDate(baseDir, checksum):
    config = SafeConfigParser()
    config.read(os.path.join(baseDir, ".global"))
    if config.has_option("application", "checksum"):
        return config.get("application", "checksum") == checksum
    else:
        return False

def getFiles(text):
    result = {}
    for line in text.split("\n"):
        if not line:
            continue 
        chksum, size, name = line.split("|")
        result[name, chksum] = int(size)
    return result
        
def update(baseDir, baseUrl, config, grabber):
    # make sure directory exists
    if not os.path.exists(baseDir):
        os.makedirs(baseDir)
    # local and remote files checksums
    if os.path.exists(os.path.join(baseDir, ".files")):
        localFiles = getFiles(open(os.path.join(baseDir, ".files"), "r").read())
    else:
        localFiles = {}
    # remote files (diable progress meter for this)
    files = grabber.urlread(baseUrl + ".files")
    remoteFiles = getFiles(files)
    # diff them
    for key in localFiles.keys():
        if key in remoteFiles:
            del remoteFiles[key]
            del localFiles[key]
    log("Files to delete:", *[name for name, cksum in localFiles])
    log("Files to download:", *[name for name, cksum in remoteFiles])
    # delete obsolete files
    for name, cksum in localFiles:
        log("Deleting file", name)
        os.remove(os.path.join(baseDir, name))
    # compute total size
    size = sum(remoteFiles.values())
    log(size, "B to download")
    # download new files
    for name, cksum in remoteFiles:
        #log("Downloading file", name)
        # make directory for file
        directory = os.path.dirname(os.path.join(baseDir, name))
        if not os.path.exists(directory):
            os.makedirs(directory)
        # download it
        grabber.urlgrab(baseUrl + name, os.path.join(baseDir, name))
    # write config
    open(os.path.join(baseDir, ".files"), "wb").write(files)
    config.write(open(os.path.join(baseDir, ".global"), "w"))

def launchApplication(baseUrl, progress):
    # init grabber
    grabber = URLGrabber(progress_obj = progress)
    # download and process application info
    log("Downloading application info")
    config = SafeConfigParser()
    data = grabber.urlread(baseUrl + ".global")
    config.readfp(StringIO(data))
    log(
        "Synchronizing application",
        config.get("application", "name"),
        config.get("application", "version"),
    )
    baseDir = getBaseDir(baseUrl)
    log("Using base directory", baseDir)
    # check if local mirror is ok
    if isUpToDate(baseDir, config.get("application", "checksum")):
        log("Application is up-to-date")
    else:
        log("Updating application")
        update(baseDir, baseUrl, config, grabber)
    # launch application
    log("Launching application")
    sys.path.insert(0, baseDir)
    os.chdir(baseDir)
    exec "import %s" % config.get("application", "module")

if __name__ == "__main__":
    from urlgrabber.progress import TextMeter
    launchApplication("http://localhost:9080/client/", TextMeter())

# vim:ts=4:sw=4:showmatch:expandtab

