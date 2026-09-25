; all paths are according to my system , do adjust all those accordingly while generating your installer

[Setup]
AppId={{B5BAF560-08C6-4A70-B7CE-F043325988D1}}
AppName=FaceRecon
AppVersion=1.0
UninstallDisplayName=FaceRecon
AppPublisher=Abhijit-71,Nwjwrbrh
AppPublisherURL=https://github.com/Nwjwrbrh/FaceRecon
AppSupportURL=https://github.com/Nwjwrbrh/FaceRecon
AppUpdatesURL=https://github.com/Nwjwrbrh/FaceRecon

; Install to Program Files
DefaultDirName={pf}\FaceRecon

; Needs admin to write associations & Program Files
PrivilegesRequired=admin

UninstallDisplayIcon={app}\FaceRecon.exe

ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

DefaultGroupName=FaceRecon

LicenseFile=LICENSE.txt

OutputBaseFilename=FaceRecon_setup


SolidCompression=yes
WizardStyle=modern


[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"


[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; \
    GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce


[Files]
; Main EXE
Source: "dist\FaceRecon\FaceRecon.exe"; \
    DestDir: "{app}"; Flags: ignoreversion

; All supporting files
Source: "dist\FaceRecon\*"; \
    DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs



[Icons]
Name: "{group}\FaceRecon"; Filename: "{app}\FaceRecon.exe"
Name: "{autodesktop}\FaceRecon"; Filename: "{app}\FaceRecon.exe"; Tasks: desktopicon


[Run]
Filename: "{app}\FaceRecon.exe"; Description: "{cm:LaunchProgram,FaceRecon}"; \
    Flags: nowait postinstall skipifsilent
