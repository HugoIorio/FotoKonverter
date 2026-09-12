[Setup]
AppName=FotoKonverter
AppVersion=1.0.0
DefaultDirName={autopf}\FotoKonverter
DefaultGroupName=FotoKonverter
UninstallDisplayIcon={app}\FotoKonverter.exe
Compression=lzma2
SolidCompression=yes
OutputBaseFilename=FotoKonverter_Setup_v1.0.0
SetupIconFile=FotoKonverter.ico

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "dist\FotoKonverter\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\FotoKonverter"; Filename: "{app}\FotoKonverter.exe"; IconFilename: "{app}\FotoKonverter.ico"
Name: "{autodesktop}\FotoKonverter"; Filename: "{app}\FotoKonverter.exe"; Tasks: desktopicon; IconFilename: "{app}\FotoKonverter.ico"

[Run]
Filename: "{app}\FotoKonverter.exe"; Description: "{cm:LaunchProgram,FotoKonverter}"; Flags: nowait postinstall skipifsilent
