from distutils.core import setup

havePy2Exe = False
try:
    import py2exe
    havePy2Exe = True
except ImportError:
    pass

import glob
import shutil
import os
import stat

# collect data files
data_files = []
data_files.append(
    (
        ".",
        ["CHANGES", "COPYING", "README"]
    )
)

# resources
for root, dirs, files in os.walk('res'):
    try:
        dirs.remove(".svn")
    except ValueError:
        pass
    if files:
        data_files.append((root, [os.path.join(root, file) for file in files]))

# version
version = (0, 2, 0)

open("oslauncher/versiondata.py", "w").write("""
#
# This is generated file, please, do not edit
#
version = %d, %d, %d
""" % version)

# setup
setup(
    name = 'outerspace',
    version = '%d.%d.%d' % version,
    description = 'Launcher for Outer Space client',
    author = "Ludek Smid",
    author_email = "qark@ospace.net",
    maintainer = 'Ludek Smid',
    maintainer_email = 'qark@ospace.net',
    url = 'http://www.ospace.net/',
    windows = [
        {
            "script": "outerspace",
            "icon_resources": [(1, "res/smallicon.ico"), (1, "res/bigicon.ico")]
        }
    ],
    data_files = data_files,
    packages = ["oslauncher", "oslauncher.urlgrabber", "oslauncher.pgu", "oslauncher.pgu.gui"],
    scripts = ["outerspace"],
)
