[Setup]
AppName=Outer Space
AppVerName=Outer Space 0.5
AppPublisher=Ludek Smid
AppVersion=0.5
AppPublisherURL=http://www.ospace.net
AppSupportURL=http://www.ospace.net
AppUpdatesURL=http://www.ospace.net
DefaultDirName={pf}\Outer Space
DefaultGroupName=Outer Space
AllowNoIcons=yes
ExtraDiskSpaceRequired=5242880
DisableStartupPrompt=yes
OutputBaseFilename=OuterSpace
OutputDir=server\website\osclient
InfoBeforeFile=license.rtf
SolidCompression=no
Compression=bzip

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"; MinVersion: 4,4
Name: "quicklaunchicon"; Description: "Create a &Quick Launch icon"; GroupDescription: "Additional icons:"; MinVersion: 4,4; Flags: unchecked

[Dirs]
Name: "{app}\var"; Flags: deleteafterinstall

[Files]
Source: "server\website\osclient\latest\*"; DestDir: "{app}"; CopyMode: alwaysoverwrite; Flags: recursesubdirs

[INI]
Filename: "{app}\osc.url"; Section: "InternetShortcut"; Key: "URL"; String: "http://www.ospace.net/"

[Icons]
Name: "{group}\Outer Space"; Filename: "{app}\osc.exe"; WorkingDir: "{app}"; IconFilename: "{app}\res\bigicon.ico"
Name: "{group}\Outer Space Web"; Filename: "{app}\osc.url"
Name: "{group}\README_CZ.TXT"; Filename: "{app}\README_CZ.TXT"
Name: "{group}\README_EN.TXT"; Filename: "{app}\README_EN.TXT"
Name: "{userdesktop}\Outer Space"; Filename: "{app}\osc.exe"; MinVersion: 4,4; Tasks: desktopicon; IconFilename: "{app}\res\bigicon.ico"
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Outer Space"; Filename: "{app}\osc.exe"; MinVersion: 4,4; Tasks: quicklaunchicon; IconFilename: "{app}\res\bigicon.ico"

[Run]
Filename: "{app}\osc.exe"; Description: "Launch Outer Space"; WorkingDir: "{app}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: files; Name: "{app}\osc.url"