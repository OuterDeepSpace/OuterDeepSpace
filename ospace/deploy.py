import sys
sys.path.append("../tools")

import os, os.path, glob
import ShellUtils
import time

baseDir = 'server/website/osclient/latest'

# generate version info
print "#\n# Generating build info\n#"


fh = open("client-pygame/lib/osci/buildInfo.py", "w")
print >> fh, """\
#
# This is generated file, please, do not edit
#
buildTime = %d
""" % (
	time.time()
)
fh.close()

# check for modified files
if 0:
    print "#\n# Checking for modified and unversioned files\n#"

    fh = os.popen("cvs -nq upd -I *.pyc")

    okToGo = True
    for line in fh:
        print line.rstrip()
        okToGo = False

    if not okToGo:
        print
        print "Fix problems displayed above and re-run deploy.py script"
        sys.exit(1)

# make directory
try:
    os.makedirs(baseDir)
except OSError:
    pass

# compile client
from compileall import compile_dir
compile_dir('client-pygame/lib')

# make binary package - SDL client
os.chdir('client-pygame')
os.system('python ..\\..\\tools\installer\Build.py _win32.spec')
os.system('python ..\\..\\tools\installer\Build.py _src.spec')
os.chdir('..')

# make binary package - wxWindows client
#os.chdir('client-msg-wx')
#os.system('python ..\\..\\tools\installer\Build.py _win32.spec')
# not used yet os.system('python ..\\..\\tools\installer\Build.py _src.spec')
#os.chdir('..')

# clean up old installation
try:
	ShellUtils.rmtree(baseDir, ignore_errors=1)
except:
	pass

ShellUtils.copytree('client-pygame/dist_win32', baseDir)
ShellUtils.copytree('client-pygame/res', os.path.join(baseDir, 'res'))
# generate new tech spec
import sys
sys.path.append('server/lib')
import ige.ospace.Rules
# copy techs specifications
os.mkdir(os.path.join(baseDir, 'res', 'techspec'))
serverSpec = "server/lib/ige/ospace/Rules"
for file in glob.glob("%s/*.spf" % serverSpec):
	ShellUtils.copy2(file, os.path.join(baseDir, 'res', 'techspec'))

# additional files
ShellUtils.copy2('updater/update.exe', baseDir)
ShellUtils.copy2('ChangeLog.txt', baseDir)
ShellUtils.copy2('README', baseDir)
ShellUtils.copy2('README_CZ', baseDir)
ShellUtils.copy2('COPYING', baseDir)

# delete binaries
#ShellUtils.rmtree('client-sdl/buildosc')
#ShellUtils.rmtree('client-sdl/distosc')

# compress executables
os.system('upx %s\\*' % baseDir)

# generate files.html
if 0:
	def listFiles(fh, base, directory):
		filelist = os.listdir(directory)
		filelist.sort()
		for file in filelist:
			if base:
				filename = base + '/' + file
			else:
				filename = file
			absfilename = os.path.join(directory, file)
			if os.path.isfile(absfilename):
				# print >> fh, '<a href="%s.bz2">%s.bz2</a><br>' % (filename, filename)
				print >> fh, '<a href="%s">%s</a><br>' % (filename, filename)
			elif os.path.isdir(absfilename):
				listFiles(fh, filename, os.path.join(directory, file))
			else:
				raise 'Unknow file type %s' % file

	fh = open(os.path.join(baseDir, 'files.html'), 'w')

	print >> fh, '''
	<html><head><title>Outer Space Client, win32 version</title></head>
	<body>
	'''

	listFiles(fh, None, baseDir)

	print >> fh, '''
	</body>
	'''

	fh.close()

# generate checksums
import md5, stat

def chsums(fh, base, directory, globalChsum):
	filelist = os.listdir(directory)
	filelist.sort()
	for file in filelist:
		if file in ('checksum.files', 'checksum.global', 'var', 'files.html'):
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
			myChsum = md5.new(data)
			print >>fh, myChsum.hexdigest(), filename, os.stat(absfilename)[stat.ST_SIZE]
		elif os.path.isdir(absfilename):
			chsums(fh, filename, os.path.join(directory, file), globalChsum)
		else:
			raise 'Unknow file type %s' % file

fh = open(os.path.join(baseDir, 'checksum.files'), 'w')
chsum = md5.new()
chsums(fh, None, baseDir, chsum)
fh.close()

fh = open(os.path.join(baseDir, 'checksum.global'), 'w')
print >>fh, chsum.hexdigest()
fh.close()

# compress files
def compress(base, directory):
	filelist = os.listdir(directory)
	filelist.sort()
	for file in filelist:
		if file in ('checksum.files', 'checksum.global', 'var', 'files.html'):
			continue
		if base:
			filename = base + '/' + file
		else:
			filename = file
		absfilename = os.path.join(directory, file)
		if os.path.isfile(absfilename):
			print 'BZIP2', os.path.normcase(absfilename)
			os.system('updater\\bzip2.exe %s' % os.path.normcase(absfilename))
		elif os.path.isdir(absfilename):
			compress(filename, os.path.join(directory, file))
		else:
			raise 'Unknow file type %s' % file

#compress(None, 'server/os_client_win32')

# create installation
os.system('..\\tools\\ISetup4\\iscc.exe setup.iss')
os.system('..\\tools\\ISetup4\\iscc.exe setup-client-msg-wx.iss')

# copy src packages
ShellUtils.copy2('client-pygame/dist_src/OuterSpace.tar.gz', "server/website/osclient/")
ShellUtils.copy2('client-pygame/dist_src/OuterSpace.zip', "server/website/osclient/")

# copy version
ShellUtils.copy2('client-pygame/lib/osci/version.py', 'server/lib/ige/ospace/ClientVersion.py')
ShellUtils.copy2('client-pygame/lib/osci/buildInfo.py', 'server/lib/ige/ospace/buildInfo.py')

# create tech tree
os.chdir("tools")
os.system("techtree.bat")
os.chdir("..")

print '#'
print '# Operation successfull'
print '#'