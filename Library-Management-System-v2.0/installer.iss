[Setup]
AppName=Library Management System
AppVersion=2.0
DefaultDirName={pf}\Library Management System
DefaultGroupName=Library Management System
OutputDir=installer
OutputBaseFilename=LibraryMS_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "dist\LibraryMS.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "data\*"; DestDir: "{app}\data"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Library Management System"; Filename: "{app}\LibraryMS.exe"
Name: "{commondesktop}\Library Management System"; Filename: "{app}\LibraryMS.exe"

[Run]
Filename: "{app}\LibraryMS.exe"; Description: "Launch Library Management System"; Flags: nowait postinstall skipifsilent