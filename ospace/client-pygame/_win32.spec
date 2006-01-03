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

a = Analysis(
	[
		os.path.join(HOMEPATH,'support\\_mountzlib.py'),
		os.path.join(HOMEPATH,'support\\useUnicode.py'),
		'osc.pyw'
	],
   pathex=['lib', '../server/lib']
)

# create distribution directory
try:
	os.mkdirs('dist_win32')
except:
	pass


# split PURE into os files and deps
import os, os.path

mydir = os.path.dirname(os.getcwd())

os = TOC()
deps = TOC()

for module, filename, type in a.pure:
	if filename[:len(mydir)] == mydir:
		os.append((module, filename, type))
	else:
		deps.append((module, filename, type))

ospyz = PYZ(os, name = "build_win32/osclib.pyz")
depspyz = PYZ(deps, name = "build_win32/deps.pyz")

exe = EXE(
	depspyz,
	a.scripts,
	exclude_binaries=1,
	name='build_win32/osc.exe',
	icon='res/bigicon.ico',
	debug=0,
	console=0,
	upx=0,
)

coll = COLLECT(
	exe,
	ospyz,
	a.binaries,
	upx=0,
	name='dist_win32'
)
