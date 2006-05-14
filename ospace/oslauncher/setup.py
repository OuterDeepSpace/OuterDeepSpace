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
version = (0, 1, 0)

# setup
setup(
    name = 'OuterSpaceLauncher',
    version = '%d.%d.%d' % version,
    description = 'Launcher of client for Outer Space',
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
    packages = ["urlgrabber", "pgu", "pgu.gui"],
    scripts = ["outerspace"],
)
