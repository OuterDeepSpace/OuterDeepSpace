# generate checksums
import os
import sha
import stat
import sys
from optparse import OptionParser
from ConfigParser import ConfigParser

def chsums(fh, base, directory, globalChsum):
    filelist = os.listdir(directory)
    filelist.sort()
    for file in filelist:
        if file in ('.files', '.global'):
            continue
        if base:
            filename = base + '/' + file
        else:
            filename = file
        absfilename = os.path.join(directory, file)
        if os.path.isfile(absfilename):
            f = open(absfilename, 'rb')
            data = f.read()
            f.close()
            globalChsum.update(data)
            myChsum = sha.new(data)
            print >>fh, "%s|%s|%s" % (myChsum.hexdigest(), os.stat(absfilename)[stat.ST_SIZE], filename)
        elif os.path.isdir(absfilename):
            chsums(fh, filename, os.path.join(directory, file), globalChsum)
        else:
            raise 'Unknow file type %s' % file


def computeChksums(basedir, name, version, module):
    fh = open(os.path.join(basedir, '.files'), 'w')
    chsum = sha.new()
    chsums(fh, None, basedir, chsum)
    fh.close()

    config = ConfigParser()
    config.add_section("application")
    config.set("application", "name", name)
    config.set("application", "version", version)
    config.set("application", "module", module)
    config.set("application", "checksum", chsum.hexdigest())
    config.write(
        open(os.path.join(basedir, '.global'), 'w')
    )

if __name__ == "__main__":
    parser = OptionParser(usage = "usage: %prog [options] DIRECTORY")
    parser.add_option("--name", action = "store", type = "string",
        dest = "name", help = "Name of application")
    parser.add_option("--version", action = "store", type = "string",
        dest = "version", help = "Version of application")
    parser.add_option("--module", action = "store", type = "string",
        dest = "module", help = "Module to import to start application")
    options, args = parser.parse_args()
    
    if len(args) != 1:
        parser.error("directory not specified")
    if not options.name:
        parser.error("--name must be specified") 
    if not options.version:
        parser.error("--version must be specified") 
    if not options.module:
        parser.error("--module must be specified") 
    computeChksums(sys.argv[1], options.name, options.version, options.module)

