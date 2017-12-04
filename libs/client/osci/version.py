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

import sys
import subprocess

revision = 0
version = (0, 0, 0, 'a')
versionString = ("%d.%d.%d%s" % version) + " [Work In Progress]"

# Here, we check if we're running as a packaged dist
if not getattr(sys, "frozen", False):
    try:
        result = subprocess.check_output(["git", "log", "-n", "1"]).split()
        versionString = result[1]
    except OSError:
        # Require GIT
        versionString = "<Unknown Version>"
