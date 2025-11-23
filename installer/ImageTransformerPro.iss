; Script for Inno Setup - Image Transformer Pro
; Version 1.0.0
; Author: Tachibana11111
; Non-commercial use only

#define MyAppName "Image Transformer Pro"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Tachibana11111"
#define MyAppURL "https://github.com/Tachibana11111"
#define MyAppExeName "Image Transformer Pro.exe"
#define MyAppEmail "truyenthonga@gmail.com"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
AppId={{DD6E7846-CAA5-4774-A565-E484CD92CD50}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
AppContact={#MyAppEmail}

; Thư mục cài đặt
DefaultDirName={autopf}\ImageTransformerPro
DefaultGroupName={#MyAppName}
AllowNoIcons=yes

; Icon
UninstallDisplayIcon={app}\{#MyAppExeName}
SetupIconFile=D:\EPU\OSS\ImageTransformerPro\installer.ico

; Kiến trúc 64-bit
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; Quyền cài đặt
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; File license và readme
LicenseFile=D:\EPU\OSS\ImageTransformerPro\license.txt
InfoBeforeFile=D:\EPU\OSS\ImageTransformerPro\readme_before.txt
InfoAfterFile=D:\EPU\OSS\ImageTransformerPro\readme_after.txt

; Output
OutputDir=D:\EPU\OSS\ImageTransformerPro\installer_output
OutputBaseFilename=ImageTransformerPro_Setup_v1.0.0

; Nén
Compression=lzma2/max
SolidCompression=yes

; Giao diện
WizardStyle=modern
DisableWelcomePage=no

; Thông tin hiển thị trong Add/Remove Programs
UninstallDisplayName={#MyAppName}
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription=Phần mềm chỉnh sửa ảnh chuyên nghiệp
VersionInfoCopyright=Copyright (C) 2025 {#MyAppPublisher}
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
Name: "quicklaunchicon"; Description: "Tạo shortcut trên Quick Launch"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; File EXE chính
Source: "D:\EPU\OSS\ImageTransformerPro\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; QUAN TRỌNG: Nếu dùng PyInstaller --onedir, uncomment dòng dưới:
; Source: "D:\EPU\OSS\ImageTransformerPro\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; File tài liệu
Source: "D:\EPU\OSS\ImageTransformerPro\README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "D:\EPU\OSS\ImageTransformerPro\license.txt"; DestDir: "{app}"; Flags: ignoreversion

; Icon (tuỳ chọn)
Source: "D:\EPU\OSS\ImageTransformerPro\installer.ico"; DestDir: "{app}"; Flags: ignoreversion

; Fonts (nếu có - uncomment nếu cần)
; Source: "D:\EPU\OSS\ImageTransformerPro\fonts\*"; DestDir: "{app}\fonts"; Flags: ignoreversion recursesubdirs

[Icons]
; Start Menu
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Comment: "Chỉnh sửa ảnh chuyên nghiệp"
Name: "{group}\Hướng dẫn sử dụng"; Filename: "{app}\README.md"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

; Desktop (nếu user chọn)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; Comment: "Chỉnh sửa ảnh chuyên nghiệp"

; Quick Launch (nếu user chọn)
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
; Chạy chương trình sau khi cài đặt
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Xóa các file tạm khi gỡ cài đặt
Type: filesandordirs; Name: "{app}\__pycache__"
Type: filesandordirs; Name: "{app}\*.pyc"
Type: filesandordirs; Name: "{app}\logs"
Type: filesandordirs; Name: "{app}\temp"

[Registry]
; Thêm vào Windows Registry
Root: HKLM; Subkey: "Software\{#MyAppPublisher}\{#MyAppName}"; Flags: uninsdeletekeyifempty
Root: HKLM; Subkey: "Software\{#MyAppPublisher}\{#MyAppName}\Settings"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"
Root: HKLM; Subkey: "Software\{#MyAppPublisher}\{#MyAppName}\Settings"; ValueType: string; ValueName: "Version"; ValueData: "{#MyAppVersion}"

[Code]
// Pascal Script - Tự động gỡ phiên bản cũ

function GetUninstallString(): String;
var
  sUnInstPath: String;
  sUnInstallString: String;
begin
  sUnInstPath := ExpandConstant('Software\Microsoft\Windows\CurrentVersion\Uninstall\{#emit SetupSetting("AppId")}_is1');
  sUnInstallString := '';
  if not RegQueryStringValue(HKLM, sUnInstPath, 'UninstallString', sUnInstallString) then
    RegQueryStringValue(HKCU, sUnInstPath, 'UninstallString', sUnInstallString);
  Result := sUnInstallString;
end;

function IsUpgrade(): Boolean;
begin
  Result := (GetUninstallString() <> '');
end;

function UnInstallOldVersion(): Integer;
var
  sUnInstallString: String;
  iResultCode: Integer;
begin
  Result := 0;
  sUnInstallString := GetUninstallString();
  if sUnInstallString <> '' then begin
    sUnInstallString := RemoveQuotes(sUnInstallString);
    if Exec(sUnInstallString, '/SILENT /NORESTART /SUPPRESSMSGBOXES','', SW_HIDE, ewWaitUntilTerminated, iResultCode) then
      Result := 3
    else
      Result := 2;
  end else
    Result := 1;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if (CurStep=ssInstall) then
  begin
    if (IsUpgrade()) then
    begin
      UnInstallOldVersion();
    end;
  end;
end;

// Hiển thị thông báo sau khi cài đặt xong
procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = wpFinished then
  begin
    // Có thể thêm custom message ở đây nếu cần
  end;
end;