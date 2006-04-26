#!/usr/bin/env python2.4
#
#  Copyright 2001 - 2006 Ludek Smid [http://www.ospace.net/]
#
#  This file is part of IGE - Outer Space.
#
#  IGE - Outer Space is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  IGE - Outer Space is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with IGE - Outer Space; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
import glob
import modulefinder
import os
import shutil
import sha
import stat
import sys
from optparse import OptionParser
from ConfigParser import ConfigParser

class Error(Exception):
    pass

def copytree(src, dst, symlinks=False):
    names = [elem for elem in os.listdir(src) if elem not in ("CVS", ".svn",)]
    os.mkdir(dst)
    errors = []
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks)
            else:
                shutil.copy2(srcname, dstname)
        except (IOError, os.error), why:
            errors.append((srcname, dstname, why))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except Error, err:
            errors.extend(err.args[0])
    if errors:
        raise Error, errors

def makeDist(distDir, module):
    # cleanup
    if os.path.exists(distDir):
        shutil.rmtree(distDir)

    # find relevant modules
    path = ["lib", "../server/lib"]

    finder = modulefinder.ModuleFinder(path = path)
    finder.run_script(module)

    # create distribution
    for name in finder.modules:
        module = finder.modules[name]
        if not module.__file__:
            continue
	if name == "__main__":
             name = "main"
        if module.__path__:
            # package
            filename = name.replace(".", "/") + "/__init__.py"
        else:
            # module
            filename = name.replace(".", "/") + ".py"
        dest = os.path.join(distDir, filename)
        # copy
        directory = os.path.dirname(dest)
        if not os.path.exists(directory):
            os.makedirs(directory)
        source = open(module.__file__, "rb").read()
        open(dest, "wb").write(source)

    # copy data files
    copytree("res", os.path.join(distDir, "res"))

    for filename in glob.glob("../server/lib/ige/ospace/Rules/*.xml"):
        shutil.copy2(filename, os.path.join(distDir, "ige/ospace/Rules"))

# generate checksums
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


def computeChksums(basedir, name, version):
    fh = open(os.path.join(basedir, '.files'), 'w')
    chsum = sha.new()
    chsums(fh, None, basedir, chsum)
    fh.close()

    config = ConfigParser()
    config.add_section("application")
    config.set("application", "name", name)
    config.set("application", "version", version)
    config.set("application", "module", "main")
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
        parser.error("--module must be specified")\
    # make distribution
    makeDist(args[0], options.module)
    # compute checksums
    computeChksums(args[0], options.name, options.version)

