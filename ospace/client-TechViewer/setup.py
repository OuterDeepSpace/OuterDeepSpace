﻿from distutils.core import setup
import py2exe, sys
sys.path.append("../server/lib")

class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        # for the versioninfo resources
        self.version = "0.2.1"
        self.company_name = "Anderuso"
        self.copyright = "(C) 2004 Anderuso"
        self.name = "OuterSpace Technology Viewer"
        self.description = "OuterSpace Technology Viewer"

manifest_template = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
<assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="x86"
    name="%(prog)s"
    type="win32"
/>
<description>%(prog)s Program</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
'''

RT_MANIFEST = 24

techViewer = Target(script = "TechViewer.py",
	other_resources = [(RT_MANIFEST, 1, manifest_template % dict(prog = "techViewer"))],
)

setup(
	windows = [techViewer],
	version = techViewer.version,
	author = techViewer.company_name,
	author_email = "anderuso@tiscali.cz",
	name = "TechViewer-src",
	url = "http://techviewer.web.tiscali.cz",
	description = techViewer.description,
    )
