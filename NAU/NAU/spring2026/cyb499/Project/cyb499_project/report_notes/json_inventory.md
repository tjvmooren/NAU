# JSON Inventory

Generated: `2026-04-29T19:17:51-07:00`

This report is for dataset inspection only. It does not create labels or build the final dataset.

Important note: files stored under `data/raw/malicious` are attack-scenario source files. Individual events should not be assumed malicious solely because of the folder they came from.

## Summary

- JSON files inspected: 48
- Files under `benign`: 3
- Files under `malicious`: 45
- Format `empty or whitespace-only`: 11
- Format `newline-delimited JSON`: 34
- Format `single JSON object`: 3

## Benign Files

### `data/raw/benign/powershell.json`

- Format: newline-delimited JSON
- Event count: 820
- Common top-level keys: `PayloadData1` (820), `PayloadData2` (820), `PayloadData3` (820), `MapDescription` (820), `ChunkNumber` (820), `Computer` (820), `Payload` (820), `Channel` (820), `Provider` (820), `EventId` (820), `EventRecordId` (820), `ProcessId` (820)
- Likely useful fields:
  - `EventID`: present in 820/820 events. Samples: `600`, `400`, `403`
  - `Provider`: present in 820/820 events. Samples: `PowerShell`
  - `Channel`: present in 820/820 events. Samples: `Windows PowerShell`
  - `TimeCreated`: present in 820/820 events. Samples: `2024-09-26T13:51:08.7231576+00:00`, `2024-09-26T13:51:08.7381230+00:00`, `2024-09-26T13:51:08.7857488+00:00`
  - `Computer`: present in 820/820 events. Samples: `Server002`
  - `CommandLine`: present in 820/820 events. Samples: `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`, `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -Command Get-Service; Get-Process`, `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -Command Get-Service;Get-Process`

### `data/raw/benign/security.json`

- Format: newline-delimited JSON
- Event count: 32761
- Common top-level keys: `ChunkNumber` (32761), `Computer` (32761), `Payload` (32761), `Channel` (32761), `Provider` (32761), `EventId` (32761), `EventRecordId` (32761), `ProcessId` (32761), `ThreadId` (32761), `Level` (32761), `Keywords` (32761), `SourceFile` (32761)
- Likely useful fields:
  - `EventID`: present in 32761/32761 events. Samples: `4624`, `4672`, `4799`
  - `Provider`: present in 32761/32761 events. Samples: `Microsoft-Windows-Security-Auditing`, `Microsoft-Windows-Eventlog`
  - `Channel`: present in 32761/32761 events. Samples: `Security`
  - `TimeCreated`: present in 32761/32761 events. Samples: `2025-04-23T19:01:06.9390403+00:00`, `2025-04-23T19:01:06.9390474+00:00`, `2025-04-23T19:01:06.9781651+00:00`
  - `Computer`: present in 32761/32761 events. Samples: `Server002`
  - `Image`: present in 1551/32761 events. Samples: `C:\Windows\System32\services.exe`, `C:\Windows\System32\svchost.exe`, `C:\Windows\System32\wininit.exe`
  - `CommandLine`: present in 16061/32761 events. Samples: `C:\Windows\System32\services.exe`, `C:\Windows\System32\svchost.exe`, `WindowsLive:(token):name=02dsuvqsngyzxykp;serviceuri=*`
  - `User`: present in 32730/32761 events. Samples: `WORKGROUP\SERVER002$`, `NT AUTHORITY\SYSTEM (S-1-5-18)`, `WORKGROUP\SERVER002$ (S-1-5-20)`

### `data/raw/benign/sysmon.json`

- Format: newline-delimited JSON
- Event count: 48125
- Common top-level keys: `PayloadData1` (48125), `MapDescription` (48125), `ChunkNumber` (48125), `Computer` (48125), `Payload` (48125), `UserId` (48125), `Channel` (48125), `Provider` (48125), `EventId` (48125), `EventRecordId` (48125), `ProcessId` (48125), `ThreadId` (48125)
- Likely useful fields:
  - `EventID`: present in 48125/48125 events. Samples: `1`, `5`, `4`
  - `Provider`: present in 48125/48125 events. Samples: `Microsoft-Windows-Sysmon`
  - `Channel`: present in 48125/48125 events. Samples: `Microsoft-Windows-Sysmon/Operational`
  - `TimeCreated`: present in 48125/48125 events. Samples: `2025-04-16T15:31:07.4112660+00:00`, `2025-04-16T15:31:08.3530585+00:00`, `2025-04-16T15:31:09.7326022+00:00`
  - `Computer`: present in 48125/48125 events. Samples: `Server002`
  - `Image`: present in 48113/48125 events. Samples: `C:\Windows\System32\wuauclt.exe`, `C:\Windows\System32\msiexec.exe`, `C:\Windows\System32\cmd.exe`
  - `CommandLine`: present in 48113/48125 events. Samples: `"C:\Windows\system32\wuauclt.exe" /UpdateDeploymentProvider UpdateDeploymentProvider.dll /ClassId f3cd146f-4abd-46f2-...`, `C:\Windows\system32\msiexec.exe /V`, `C:\Windows\system32\cmd.exe /c RD /S /Q C:\ProgramData\PLUG`
  - `ParentImage`: present in 20738/48125 events. Samples: `C:\Windows\System32\msiexec.exe`, `C:\Windows\System32\cmd.exe`, `C:\Windows\SysWOW64\schtasks.exe`
  - `User`: present in 48113/48125 events. Samples: `NT AUTHORITY\SYSTEM`, `SERVER002\lplui`, `NT AUTHORITY\NETWORK SERVICE`


## Malicious Files

### `data/raw/malicious/c2c_dns_https_largequeryvolume_json/T1572-1_Application.json`

- Format: newline-delimited JSON
- Event count: 3
- Common top-level keys: `Event` (3)
- Likely useful fields:
  - `EventID`: present in 3/3 events. Samples: `16384`, `0`
  - `Provider`: present in 3/3 events. Samples: `Microsoft-Windows-Security-SPP`, `edgeupdate`
  - `Channel`: present in 3/3 events. Samples: `Application`
  - `TimeCreated`: present in 3/3 events. Samples: `2024-10-28 15:11:27.4245288`, `2024-10-28 15:11:32.0975109`, `2024-10-28 15:11:34.6344939`
  - `Computer`: present in 3/3 events. Samples: `Server002`

### `data/raw/malicious/c2c_dns_https_largequeryvolume_json/T1572-1_Microsoft-Windows-Sysmon_Operational.json`

- Format: newline-delimited JSON
- Event count: 55
- Common top-level keys: `Event` (55)
- Likely useful fields:
  - `EventID`: present in 55/55 events. Samples: `1`, `5`
  - `Provider`: present in 55/55 events. Samples: `Microsoft-Windows-Sysmon`
  - `Channel`: present in 55/55 events. Samples: `Microsoft-Windows-Sysmon/Operational`
  - `TimeCreated`: present in 55/55 events. Samples: `2024-10-28 15:11:09.5248246`, `2024-10-28 15:11:09.5275513`, `2024-10-28 15:11:09.5592452`
  - `Computer`: present in 55/55 events. Samples: `Server002`
  - `Image`: present in 55/55 events. Samples: `C:\Windows\System32\HOSTNAME.EXE`, `C:\Windows\System32\conhost.exe`, `C:\Windows\System32\whoami.exe`
  - `CommandLine`: present in 29/55 events. Samples: `"C:\Windows\system32\HOSTNAME.EXE"`, `\??\C:\Windows\system32\conhost.exe 0xffffffff -ForceV1`, `"C:\Windows\system32\whoami.exe"`
  - `ParentImage`: present in 21/55 events. Samples: `C:\Windows\System32\wsmprovhost.exe`, `C:\Windows\System32\HOSTNAME.EXE`, `C:\Windows\System32\whoami.exe`
  - `User`: present in 55/55 events. Samples: `SERVER002\admin_test`, `NT AUTHORITY\SYSTEM`, `NT AUTHORITY\NETWORK SERVICE`

### `data/raw/malicious/c2c_dns_https_largequeryvolume_json/T1572-1_Security.json`

- Format: newline-delimited JSON
- Event count: 9
- Common top-level keys: `Event` (9)
- Likely useful fields:
  - `EventID`: present in 9/9 events. Samples: `4616`, `4624`, `4672`
  - `Provider`: present in 9/9 events. Samples: `Microsoft-Windows-Security-Auditing`
  - `Channel`: present in 9/9 events. Samples: `Security`
  - `TimeCreated`: present in 9/9 events. Samples: `2024-10-28 15:11:15.5299449`, `2024-10-28 15:11:15.5309225`, `2024-10-28 15:13:18.3556627`
  - `Computer`: present in 9/9 events. Samples: `Server002`
  - `Image`: present in 3/9 events. Samples: `C:\Windows\System32\svchost.exe`, `C:\Windows\System32\services.exe`
  - `User`: present in 9/9 events. Samples: `LOCAL SERVICE`, `SYSTEM`, `admin_test`

### `data/raw/malicious/c2c_dns_https_largequeryvolume_json/T1572-1_System.json`

- Format: newline-delimited JSON
- Event count: 5
- Common top-level keys: `Event` (5)
- Likely useful fields:
  - `EventID`: present in 5/5 events. Samples: `24`, `1`, `35`
  - `Provider`: present in 5/5 events. Samples: `Microsoft-Windows-Kernel-General`, `Microsoft-Windows-Time-Service`
  - `Channel`: present in 5/5 events. Samples: `System`
  - `TimeCreated`: present in 5/5 events. Samples: `2024-10-28 15:11:15.5296151`, `2024-10-28 15:11:15.5297842`, `2024-10-28 15:11:15.5304867`
  - `Computer`: present in 5/5 events. Samples: `Server002`
  - `Image`: present in 2/5 events. Samples: `\Device\HarddiskVolume2\Windows\System32\svchost.exe`

### `data/raw/malicious/c2c_dns_https_largequeryvolume_json/T1572-1_Windows PowerShell.json`

- Format: newline-delimited JSON
- Event count: 7
- Common top-level keys: `Event` (7)
- Likely useful fields:
  - `EventID`: present in 7/7 events. Samples: `600`, `400`
  - `Provider`: present in 7/7 events. Samples: `PowerShell`
  - `Channel`: present in 7/7 events. Samples: `Windows PowerShell`
  - `TimeCreated`: present in 7/7 events. Samples: `2024-10-28 15:11:15.6852996`, `2024-10-28 15:11:15.6944085`, `2024-10-28 15:11:15.6989974`
  - `Computer`: present in 7/7 events. Samples: `Server002`
  - `CommandLine`: present in 7/7 events. Samples: `powershell.exe & {for($i=0; $i -le 1000; $i++) { (Invoke-WebRequest "https://8.8.8.8/resolve?name=file.$(Get-Random -...`

### `data/raw/malicious/collection_compressData_lockwithpw_exfiltrationwinrar_json/T1560.001-2_Application.json`

- Format: newline-delimited JSON
- Event count: 3
- Common top-level keys: `Event` (3)
- Likely useful fields:
  - `EventID`: present in 3/3 events. Samples: `0`, `15`
  - `Provider`: present in 3/3 events. Samples: `edgeupdate`, `SecurityCenter`
  - `Channel`: present in 3/3 events. Samples: `Application`
  - `TimeCreated`: present in 3/3 events. Samples: `2024-10-28 07:49:41.1601750`, `2024-10-28 07:49:45.1543359`, `2024-10-28 07:50:05.6294563`
  - `Computer`: present in 3/3 events. Samples: `Server002`

### `data/raw/malicious/collection_compressData_lockwithpw_exfiltrationwinrar_json/T1560.001-2_Microsoft-Windows-Sysmon_Operational.json`

- Format: newline-delimited JSON
- Event count: 43
- Common top-level keys: `Event` (43)
- Likely useful fields:
  - `EventID`: present in 43/43 events. Samples: `1`, `5`
  - `Provider`: present in 43/43 events. Samples: `Microsoft-Windows-Sysmon`
  - `Channel`: present in 43/43 events. Samples: `Microsoft-Windows-Sysmon/Operational`
  - `TimeCreated`: present in 43/43 events. Samples: `2024-10-28 07:49:38.2576729`, `2024-10-28 07:49:38.3326795`, `2024-10-28 07:49:38.3763644`
  - `Computer`: present in 43/43 events. Samples: `Server002`
  - `Image`: present in 43/43 events. Samples: `C:\Program Files (x86)\Microsoft\Temp\EU6D66.tmp\MicrosoftEdgeUpdate.exe`, `C:\Windows\System32\cmd.exe`, `C:\Windows\System32\SecurityHealthService.exe`
  - `CommandLine`: present in 23/43 events. Samples: `"C:\Program Files (x86)\Microsoft\Temp\EU6D66.tmp\MicrosoftEdgeUpdate.exe" /update /sessionid "{68B584D5-333A-4054-A5...`, `C:\Windows\system32\SecurityHealthService.exe`, `"cmd.exe" /c if not exist "%%programfiles%%/WinRAR/Rar.exe" (exit /b 1)`
  - `ParentImage`: present in 20/43 events. Samples: `C:\Program Files (x86)\Microsoft\EdgeUpdate\Install\{34AB67C2-1802-47E2-A7BA-8D2B8E16F442}\MicrosoftEdgeUpdateSetup_X...`, `C:\Windows\System32\wsmprovhost.exe`, `C:\Windows\System32\cmd.exe`
  - `User`: present in 43/43 events. Samples: `NT AUTHORITY\SYSTEM`, `SERVER002\admin_test`

### `data/raw/malicious/collection_compressData_lockwithpw_exfiltrationwinrar_json/T1560.001-2_Security.json`

- Format: newline-delimited JSON
- Event count: 2
- Common top-level keys: `Event` (2)
- Likely useful fields:
  - `EventID`: present in 2/2 events. Samples: `4624`, `4672`
  - `Provider`: present in 2/2 events. Samples: `Microsoft-Windows-Security-Auditing`
  - `Channel`: present in 2/2 events. Samples: `Security`
  - `TimeCreated`: present in 2/2 events. Samples: `2024-10-28 07:49:38.3519199`, `2024-10-28 07:49:38.3519253`
  - `Computer`: present in 2/2 events. Samples: `Server002`
  - `Image`: present in 1/2 events. Samples: `C:\Windows\System32\services.exe`
  - `User`: present in 2/2 events. Samples: `SYSTEM`

### `data/raw/malicious/collection_compressData_lockwithpw_exfiltrationwinrar_json/T1560.001-2_System.json`

- Format: empty or whitespace-only
- Event count: 0
- Common top-level keys: none
- Likely useful fields: none extracted
- Note: File is empty or contains only whitespace/BOM content.

### `data/raw/malicious/collection_compressData_lockwithpw_exfiltrationwinrar_json/T1560.001-2_Windows PowerShell.json`

- Format: empty or whitespace-only
- Event count: 0
- Common top-level keys: none
- Likely useful fields: none extracted
- Note: File is empty or contains only whitespace/BOM content.

### `data/raw/malicious/credential-access-bruteforceCreds_singleActiveDirectory_viaLDAP_json/T1110.001-2_Application.json`

- Format: single JSON object
- Event count: 1
- Common top-level keys: `Event` (1)
- Likely useful fields:
  - `EventID`: present in 1/1 events. Samples: `16384`
  - `Provider`: present in 1/1 events. Samples: `Microsoft-Windows-Security-SPP`
  - `Channel`: present in 1/1 events. Samples: `Application`
  - `TimeCreated`: present in 1/1 events. Samples: `2024-10-24 13:19:32.5480511`
  - `Computer`: present in 1/1 events. Samples: `Server002`
- Note: Loaded as a single JSON object. This file is not NDJSON or a JSON array.

### `data/raw/malicious/credential-access-bruteforceCreds_singleActiveDirectory_viaLDAP_json/T1110.001-2_Microsoft-Windows-Sysmon_Operational.json`

- Format: newline-delimited JSON
- Event count: 15
- Common top-level keys: `Event` (15)
- Likely useful fields:
  - `EventID`: present in 15/15 events. Samples: `1`, `5`
  - `Provider`: present in 15/15 events. Samples: `Microsoft-Windows-Sysmon`
  - `Channel`: present in 15/15 events. Samples: `Microsoft-Windows-Sysmon/Operational`
  - `TimeCreated`: present in 15/15 events. Samples: `2024-10-24 13:19:17.3860068`, `2024-10-24 13:19:17.3917316`, `2024-10-24 13:19:17.4296871`
  - `Computer`: present in 15/15 events. Samples: `Server002`
  - `Image`: present in 15/15 events. Samples: `C:\Windows\System32\HOSTNAME.EXE`, `C:\Windows\System32\conhost.exe`, `C:\Windows\System32\whoami.exe`
  - `CommandLine`: present in 6/15 events. Samples: `"C:\Windows\system32\HOSTNAME.EXE"`, `\??\C:\Windows\system32\conhost.exe 0xffffffff -ForceV1`, `"C:\Windows\system32\whoami.exe"`
  - `ParentImage`: present in 6/15 events. Samples: `C:\Windows\System32\wsmprovhost.exe`, `C:\Windows\System32\HOSTNAME.EXE`, `C:\Windows\System32\whoami.exe`
  - `User`: present in 15/15 events. Samples: `SERVER002\admin_test`, `NT AUTHORITY\SYSTEM`, `NT AUTHORITY\NETWORK SERVICE`

### `data/raw/malicious/credential-access-bruteforceCreds_singleActiveDirectory_viaLDAP_json/T1110.001-2_Security.json`

- Format: newline-delimited JSON
- Event count: 2
- Common top-level keys: `Event` (2)
- Likely useful fields:
  - `EventID`: present in 2/2 events. Samples: `4616`
  - `Provider`: present in 2/2 events. Samples: `Microsoft-Windows-Security-Auditing`
  - `Channel`: present in 2/2 events. Samples: `Security`
  - `TimeCreated`: present in 2/2 events. Samples: `2024-10-24 13:19:17.0616986`, `2024-10-24 13:19:17.0626865`
  - `Computer`: present in 2/2 events. Samples: `Server002`
  - `Image`: present in 2/2 events. Samples: `C:\Windows\System32\svchost.exe`
  - `User`: present in 2/2 events. Samples: `LOCAL SERVICE`

### `data/raw/malicious/credential-access-bruteforceCreds_singleActiveDirectory_viaLDAP_json/T1110.001-2_System.json`

- Format: newline-delimited JSON
- Event count: 5
- Common top-level keys: `Event` (5)
- Likely useful fields:
  - `EventID`: present in 5/5 events. Samples: `24`, `1`, `35`
  - `Provider`: present in 5/5 events. Samples: `Microsoft-Windows-Kernel-General`, `Microsoft-Windows-Time-Service`
  - `Channel`: present in 5/5 events. Samples: `System`
  - `TimeCreated`: present in 5/5 events. Samples: `2024-10-24 13:19:17.0611894`, `2024-10-24 13:19:17.0614131`, `2024-10-24 13:19:17.0622410`
  - `Computer`: present in 5/5 events. Samples: `Server002`
  - `Image`: present in 2/5 events. Samples: `\Device\HarddiskVolume2\Windows\System32\svchost.exe`

### `data/raw/malicious/credential-access-bruteforceCreds_singleActiveDirectory_viaLDAP_json/T1110.001-2_Windows PowerShell.json`

- Format: newline-delimited JSON
- Event count: 8
- Common top-level keys: `Event` (8)
- Likely useful fields:
  - `EventID`: present in 8/8 events. Samples: `600`, `400`, `403`
  - `Provider`: present in 8/8 events. Samples: `PowerShell`
  - `Channel`: present in 8/8 events. Samples: `Windows PowerShell`
  - `TimeCreated`: present in 8/8 events. Samples: `2024-10-24 13:19:18.4638733`, `2024-10-24 13:19:18.5122741`, `2024-10-24 13:19:18.5215770`
  - `Computer`: present in 8/8 events. Samples: `Server002`
  - `CommandLine`: present in 8/8 events. Samples: `powershell.exe & {if ("NTLM".ToLower() -NotIn @("ntlm","kerberos")) {`

### `data/raw/malicious/defense_evasion_disable_windows_registry_tool_json/T1112-10_Application.json`

- Format: single JSON object
- Event count: 1
- Common top-level keys: `Event` (1)
- Likely useful fields:
  - `EventID`: present in 1/1 events. Samples: `0`
  - `Provider`: present in 1/1 events. Samples: `edgeupdate`
  - `Channel`: present in 1/1 events. Samples: `Application`
  - `TimeCreated`: present in 1/1 events. Samples: `2024-10-24 14:46:46.4781711`
  - `Computer`: present in 1/1 events. Samples: `Server002`
- Note: Loaded as a single JSON object. This file is not NDJSON or a JSON array.

### `data/raw/malicious/defense_evasion_disable_windows_registry_tool_json/T1112-10_Microsoft-Windows-Sysmon_Operational.json`

- Format: newline-delimited JSON
- Event count: 22
- Common top-level keys: `Event` (22)
- Likely useful fields:
  - `EventID`: present in 22/22 events. Samples: `1`, `5`
  - `Provider`: present in 22/22 events. Samples: `Microsoft-Windows-Sysmon`
  - `Channel`: present in 22/22 events. Samples: `Microsoft-Windows-Sysmon/Operational`
  - `TimeCreated`: present in 22/22 events. Samples: `2024-10-24 14:45:59.4579571`, `2024-10-24 14:45:59.4642813`, `2024-10-24 14:45:59.5180805`
  - `Computer`: present in 22/22 events. Samples: `Server002`
  - `Image`: present in 22/22 events. Samples: `C:\Windows\System32\HOSTNAME.EXE`, `C:\Windows\System32\conhost.exe`, `C:\Windows\System32\whoami.exe`
  - `CommandLine`: present in 10/22 events. Samples: `"C:\Windows\system32\HOSTNAME.EXE"`, `\??\C:\Windows\system32\conhost.exe 0xffffffff -ForceV1`, `"C:\Windows\system32\whoami.exe"`
  - `ParentImage`: present in 9/22 events. Samples: `C:\Windows\System32\wsmprovhost.exe`, `C:\Windows\System32\HOSTNAME.EXE`, `C:\Windows\System32\whoami.exe`
  - `User`: present in 22/22 events. Samples: `SERVER002\admin_test`, `NT AUTHORITY\SYSTEM`

### `data/raw/malicious/defense_evasion_disable_windows_registry_tool_json/T1112-10_Security.json`

- Format: newline-delimited JSON
- Event count: 2
- Common top-level keys: `Event` (2)
- Likely useful fields:
  - `EventID`: present in 2/2 events. Samples: `4616`
  - `Provider`: present in 2/2 events. Samples: `Microsoft-Windows-Security-Auditing`
  - `Channel`: present in 2/2 events. Samples: `Security`
  - `TimeCreated`: present in 2/2 events. Samples: `2024-10-24 14:46:19.8663915`, `2024-10-24 14:46:19.8682187`
  - `Computer`: present in 2/2 events. Samples: `Server002`
  - `Image`: present in 2/2 events. Samples: `C:\Windows\System32\svchost.exe`
  - `User`: present in 2/2 events. Samples: `LOCAL SERVICE`

### `data/raw/malicious/defense_evasion_disable_windows_registry_tool_json/T1112-10_System.json`

- Format: newline-delimited JSON
- Event count: 5
- Common top-level keys: `Event` (5)
- Likely useful fields:
  - `EventID`: present in 5/5 events. Samples: `24`, `1`, `35`
  - `Provider`: present in 5/5 events. Samples: `Microsoft-Windows-Kernel-General`, `Microsoft-Windows-Time-Service`
  - `Channel`: present in 5/5 events. Samples: `System`
  - `TimeCreated`: present in 5/5 events. Samples: `2024-10-24 14:46:19.8657624`, `2024-10-24 14:46:19.8660716`, `2024-10-24 14:46:19.8669075`
  - `Computer`: present in 5/5 events. Samples: `Server002`
  - `Image`: present in 2/5 events. Samples: `\Device\HarddiskVolume2\Windows\System32\svchost.exe`

### `data/raw/malicious/defense_evasion_disable_windows_registry_tool_json/T1112-10_Windows PowerShell.json`

- Format: empty or whitespace-only
- Event count: 0
- Common top-level keys: none
- Likely useful fields: none extracted
- Note: File is empty or contains only whitespace/BOM content.

### `data/raw/malicious/discovery_discover_system_language_withchcp_json/T1614.001-2_Application.json`

- Format: single JSON object
- Event count: 1
- Common top-level keys: `Event` (1)
- Likely useful fields:
  - `EventID`: present in 1/1 events. Samples: `16384`
  - `Provider`: present in 1/1 events. Samples: `Microsoft-Windows-Security-SPP`
  - `Channel`: present in 1/1 events. Samples: `Application`
  - `TimeCreated`: present in 1/1 events. Samples: `2024-10-28 16:21:04.0226494`
  - `Computer`: present in 1/1 events. Samples: `Server002`
- Note: Loaded as a single JSON object. This file is not NDJSON or a JSON array.

### `data/raw/malicious/discovery_discover_system_language_withchcp_json/T1614.001-2_Microsoft-Windows-Sysmon_Operational.json`

- Format: newline-delimited JSON
- Event count: 19
- Common top-level keys: `Event` (19)
- Likely useful fields:
  - `EventID`: present in 19/19 events. Samples: `1`, `5`
  - `Provider`: present in 19/19 events. Samples: `Microsoft-Windows-Sysmon`
  - `Channel`: present in 19/19 events. Samples: `Microsoft-Windows-Sysmon/Operational`
  - `TimeCreated`: present in 19/19 events. Samples: `2024-10-28 16:20:50.3980966`, `2024-10-28 16:20:50.4048385`, `2024-10-28 16:20:50.4669497`
  - `Computer`: present in 19/19 events. Samples: `Server002`
  - `Image`: present in 19/19 events. Samples: `C:\Windows\System32\HOSTNAME.EXE`, `C:\Windows\System32\conhost.exe`, `C:\Windows\System32\whoami.exe`
  - `CommandLine`: present in 7/19 events. Samples: `"C:\Windows\system32\HOSTNAME.EXE"`, `\??\C:\Windows\system32\conhost.exe 0xffffffff -ForceV1`, `"C:\Windows\system32\whoami.exe"`
  - `ParentImage`: present in 4/19 events. Samples: `C:\Windows\System32\HOSTNAME.EXE`, `C:\Windows\System32\whoami.exe`, `C:\Windows\System32\cmd.exe`
  - `User`: present in 19/19 events. Samples: `SERVER002\admin_test`, `NT AUTHORITY\SYSTEM`, `NT AUTHORITY\NETWORK SERVICE`

### `data/raw/malicious/discovery_discover_system_language_withchcp_json/T1614.001-2_Security.json`

- Format: newline-delimited JSON
- Event count: 7
- Common top-level keys: `Event` (7)
- Likely useful fields:
  - `EventID`: present in 7/7 events. Samples: `4616`, `4634`, `4672`
  - `Provider`: present in 7/7 events. Samples: `Microsoft-Windows-Security-Auditing`
  - `Channel`: present in 7/7 events. Samples: `Security`
  - `TimeCreated`: present in 7/7 events. Samples: `2024-10-28 16:20:49.9662583`, `2024-10-28 16:20:49.9674902`, `2024-10-28 16:20:50.3489351`
  - `Computer`: present in 7/7 events. Samples: `Server002`
  - `Image`: present in 2/7 events. Samples: `C:\Windows\System32\svchost.exe`
  - `User`: present in 7/7 events. Samples: `LOCAL SERVICE`, `admin_test`

### `data/raw/malicious/discovery_discover_system_language_withchcp_json/T1614.001-2_System.json`

- Format: newline-delimited JSON
- Event count: 5
- Common top-level keys: `Event` (5)
- Likely useful fields:
  - `EventID`: present in 5/5 events. Samples: `24`, `1`, `35`
  - `Provider`: present in 5/5 events. Samples: `Microsoft-Windows-Kernel-General`, `Microsoft-Windows-Time-Service`
  - `Channel`: present in 5/5 events. Samples: `System`
  - `TimeCreated`: present in 5/5 events. Samples: `2024-10-28 16:20:49.9655739`, `2024-10-28 16:20:49.9659134`, `2024-10-28 16:20:49.9668201`
  - `Computer`: present in 5/5 events. Samples: `Server002`
  - `Image`: present in 2/5 events. Samples: `\Device\HarddiskVolume2\Windows\System32\svchost.exe`

### `data/raw/malicious/discovery_discover_system_language_withchcp_json/T1614.001-2_Windows PowerShell.json`

- Format: empty or whitespace-only
- Event count: 0
- Common top-level keys: none
- Likely useful fields: none extracted
- Note: File is empty or contains only whitespace/BOM content.

### `data/raw/malicious/execute-powershell-script-via-word-dde-json/T1559.002-2_Application.json`

- Format: newline-delimited JSON
- Event count: 2
- Common top-level keys: `Event` (2)
- Likely useful fields:
  - `EventID`: present in 2/2 events. Samples: `0`
  - `Provider`: present in 2/2 events. Samples: `edgeupdate`
  - `Channel`: present in 2/2 events. Samples: `Application`
  - `TimeCreated`: present in 2/2 events. Samples: `2024-10-28 07:38:20.8493815`, `2024-10-28 07:38:23.4228574`
  - `Computer`: present in 2/2 events. Samples: `Server002`

### `data/raw/malicious/execute-powershell-script-via-word-dde-json/T1559.002-2_Microsoft-Windows-Sysmon_Operational.json`

- Format: newline-delimited JSON
- Event count: 46
- Common top-level keys: `Event` (46)
- Likely useful fields:
  - `EventID`: present in 46/46 events. Samples: `1`, `5`
  - `Provider`: present in 46/46 events. Samples: `Microsoft-Windows-Sysmon`
  - `Channel`: present in 46/46 events. Samples: `Microsoft-Windows-Sysmon/Operational`
  - `TimeCreated`: present in 46/46 events. Samples: `2024-10-28 07:38:11.3788339`, `2024-10-28 07:38:11.3822513`, `2024-10-28 07:38:11.4116630`
  - `Computer`: present in 46/46 events. Samples: `Server002`
  - `Image`: present in 46/46 events. Samples: `C:\Windows\System32\HOSTNAME.EXE`, `C:\Windows\System32\conhost.exe`, `C:\Windows\System32\whoami.exe`
  - `CommandLine`: present in 23/46 events. Samples: `"C:\Windows\system32\HOSTNAME.EXE"`, `\??\C:\Windows\system32\conhost.exe 0xffffffff -ForceV1`, `"C:\Windows\system32\whoami.exe"`
  - `ParentImage`: present in 20/46 events. Samples: `C:\Windows\System32\wsmprovhost.exe`, `C:\Windows\System32\HOSTNAME.EXE`, `C:\Windows\System32\whoami.exe`
  - `User`: present in 46/46 events. Samples: `SERVER002\admin_test`, `NT AUTHORITY\SYSTEM`

### `data/raw/malicious/execute-powershell-script-via-word-dde-json/T1559.002-2_Security.json`

- Format: newline-delimited JSON
- Event count: 9
- Common top-level keys: `Event` (9)
- Likely useful fields:
  - `EventID`: present in 9/9 events. Samples: `4616`, `5379`
  - `Provider`: present in 9/9 events. Samples: `Microsoft-Windows-Security-Auditing`
  - `Channel`: present in 9/9 events. Samples: `Security`
  - `TimeCreated`: present in 9/9 events. Samples: `2024-10-28 07:38:16.6161439`, `2024-10-28 07:38:16.6171163`, `2024-10-28 07:38:19.8275640`
  - `Computer`: present in 9/9 events. Samples: `Server002`
  - `Image`: present in 2/9 events. Samples: `C:\Windows\System32\svchost.exe`
  - `User`: present in 9/9 events. Samples: `LOCAL SERVICE`, `SERVER002$`

### `data/raw/malicious/execute-powershell-script-via-word-dde-json/T1559.002-2_System.json`

- Format: newline-delimited JSON
- Event count: 5
- Common top-level keys: `Event` (5)
- Likely useful fields:
  - `EventID`: present in 5/5 events. Samples: `24`, `1`, `35`
  - `Provider`: present in 5/5 events. Samples: `Microsoft-Windows-Kernel-General`, `Microsoft-Windows-Time-Service`
  - `Channel`: present in 5/5 events. Samples: `System`
  - `TimeCreated`: present in 5/5 events. Samples: `2024-10-28 07:38:16.6158572`, `2024-10-28 07:38:16.6160275`, `2024-10-28 07:38:16.6166206`
  - `Computer`: present in 5/5 events. Samples: `Server002`
  - `Image`: present in 2/5 events. Samples: `\Device\HarddiskVolume2\Windows\System32\svchost.exe`

### `data/raw/malicious/execute-powershell-script-via-word-dde-json/T1559.002-2_Windows PowerShell.json`

- Format: empty or whitespace-only
- Event count: 0
- Common top-level keys: none
- Likely useful fields: none extracted
- Note: File is empty or contains only whitespace/BOM content.

### `data/raw/malicious/execution-app-uninstall-using-wmic-json/T1047-10_Application.json`

- Format: newline-delimited JSON
- Event count: 2
- Common top-level keys: `Event` (2)
- Likely useful fields:
  - `EventID`: present in 2/2 events. Samples: `1035`
  - `Provider`: present in 2/2 events. Samples: `MsiInstaller`
  - `Channel`: present in 2/2 events. Samples: `Application`
  - `TimeCreated`: present in 2/2 events. Samples: `2024-10-22 15:28:03.3052455`, `2024-10-22 15:28:03.3848039`
  - `Computer`: present in 2/2 events. Samples: `Server002`

### `data/raw/malicious/execution-app-uninstall-using-wmic-json/T1047-10_Microsoft-Windows-Sysmon_Operational.json`

- Format: newline-delimited JSON
- Event count: 20
- Common top-level keys: `Event` (20)
- Likely useful fields:
  - `EventID`: present in 20/20 events. Samples: `5`, `1`
  - `Provider`: present in 20/20 events. Samples: `Microsoft-Windows-Sysmon`
  - `Channel`: present in 20/20 events. Samples: `Microsoft-Windows-Sysmon/Operational`
  - `TimeCreated`: present in 20/20 events. Samples: `2024-10-22 15:27:58.0734188`, `2024-10-22 15:27:58.0928462`, `2024-10-22 15:28:00.2979987`
  - `Computer`: present in 20/20 events. Samples: `Server002`
  - `Image`: present in 20/20 events. Samples: `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`, `C:\Windows\System32\conhost.exe`, `C:\Windows\System32\HOSTNAME.EXE`
  - `CommandLine`: present in 11/20 events. Samples: `"C:\Windows\system32\HOSTNAME.EXE"`, `\??\C:\Windows\system32\conhost.exe 0xffffffff -ForceV1`, `"C:\Windows\system32\whoami.exe"`
  - `ParentImage`: present in 10/20 events. Samples: `C:\Windows\System32\wsmprovhost.exe`, `C:\Windows\System32\HOSTNAME.EXE`, `C:\Windows\System32\whoami.exe`
  - `User`: present in 20/20 events. Samples: `SERVER002\admin_test`, `NT AUTHORITY\SYSTEM`

### `data/raw/malicious/execution-app-uninstall-using-wmic-json/T1047-10_Security.json`

- Format: empty or whitespace-only
- Event count: 0
- Common top-level keys: none
- Likely useful fields: none extracted
- Note: File is empty or contains only whitespace/BOM content.

### `data/raw/malicious/execution-app-uninstall-using-wmic-json/T1047-10_System.json`

- Format: empty or whitespace-only
- Event count: 0
- Common top-level keys: none
- Likely useful fields: none extracted
- Note: File is empty or contains only whitespace/BOM content.

### `data/raw/malicious/execution-app-uninstall-using-wmic-json/T1047-10_Windows PowerShell.json`

- Format: empty or whitespace-only
- Event count: 0
- Common top-level keys: none
- Likely useful fields: none extracted
- Note: File is empty or contains only whitespace/BOM content.

### `data/raw/malicious/lateral_powershell_lateral_usingExcelAppObject_Json/T1021.003-2_Application.json`

- Format: empty or whitespace-only
- Event count: 0
- Common top-level keys: none
- Likely useful fields: none extracted
- Note: File is empty or contains only whitespace/BOM content.

### `data/raw/malicious/lateral_powershell_lateral_usingExcelAppObject_Json/T1021.003-2_Microsoft-Windows-Sysmon_Operational.json`

- Format: newline-delimited JSON
- Event count: 22
- Common top-level keys: `Event` (22)
- Likely useful fields:
  - `EventID`: present in 22/22 events. Samples: `5`, `1`
  - `Provider`: present in 22/22 events. Samples: `Microsoft-Windows-Sysmon`
  - `Channel`: present in 22/22 events. Samples: `Microsoft-Windows-Sysmon/Operational`
  - `TimeCreated`: present in 22/22 events. Samples: `2024-10-21 11:24:59.4799625`, `2024-10-21 11:24:59.4812668`, `2024-10-21 11:25:00.0522312`
  - `Computer`: present in 22/22 events. Samples: `Server002`
  - `Image`: present in 22/22 events. Samples: `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`, `C:\Windows\System32\conhost.exe`, `C:\Windows\System32\HOSTNAME.EXE`
  - `CommandLine`: present in 13/22 events. Samples: `"C:\Windows\system32\HOSTNAME.EXE"`, `\??\C:\Windows\system32\conhost.exe 0xffffffff -ForceV1`, `"C:\Windows\system32\whoami.exe"`
  - `ParentImage`: present in 9/22 events. Samples: `C:\Windows\System32\HOSTNAME.EXE`, `C:\Windows\System32\whoami.exe`, `C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`
  - `User`: present in 22/22 events. Samples: `SERVER002\admin_test`, `NT AUTHORITY\SYSTEM`

### `data/raw/malicious/lateral_powershell_lateral_usingExcelAppObject_Json/T1021.003-2_Security.json`

- Format: empty or whitespace-only
- Event count: 0
- Common top-level keys: none
- Likely useful fields: none extracted
- Note: File is empty or contains only whitespace/BOM content.

### `data/raw/malicious/lateral_powershell_lateral_usingExcelAppObject_Json/T1021.003-2_System.json`

- Format: newline-delimited JSON
- Event count: 3
- Common top-level keys: `Event` (3)
- Likely useful fields:
  - `EventID`: present in 3/3 events. Samples: `44`, `43`, `19`
  - `Provider`: present in 3/3 events. Samples: `Microsoft-Windows-WindowsUpdateClient`
  - `Channel`: present in 3/3 events. Samples: `System`
  - `TimeCreated`: present in 3/3 events. Samples: `2024-10-21 11:25:08.1347919`, `2024-10-21 11:25:12.1771267`, `2024-10-21 11:25:43.6152524`
  - `Computer`: present in 3/3 events. Samples: `Server002`

### `data/raw/malicious/lateral_powershell_lateral_usingExcelAppObject_Json/T1021.003-2_Windows PowerShell.json`

- Format: newline-delimited JSON
- Event count: 9
- Common top-level keys: `Event` (9)
- Likely useful fields:
  - `EventID`: present in 9/9 events. Samples: `600`, `400`, `300`
  - `Provider`: present in 9/9 events. Samples: `PowerShell`
  - `Channel`: present in 9/9 events. Samples: `Windows PowerShell`
  - `TimeCreated`: present in 9/9 events. Samples: `2024-10-21 11:25:00.9418620`, `2024-10-21 11:25:01.0004325`, `2024-10-21 11:25:01.3198313`
  - `Computer`: present in 9/9 events. Samples: `Server002`
  - `CommandLine`: present in 9/9 events. Samples: `powershell.exe & {copy c:\windows\system32\calc.exe 'C:\users\admin\AppData\local\Microsoft\WindowsApps\foxprow.exe'`

### `data/raw/malicious/persistence_persist_download_execute_json/T1197-3_Application.json`

- Format: newline-delimited JSON
- Event count: 3
- Common top-level keys: `Event` (3)
- Likely useful fields:
  - `EventID`: present in 3/3 events. Samples: `16384`, `0`
  - `Provider`: present in 3/3 events. Samples: `Microsoft-Windows-Security-SPP`, `edgeupdate`
  - `Channel`: present in 3/3 events. Samples: `Application`
  - `TimeCreated`: present in 3/3 events. Samples: `2024-10-25 17:03:09.6669424`, `2024-10-25 17:03:28.5303570`, `2024-10-25 17:03:30.8773802`
  - `Computer`: present in 3/3 events. Samples: `Server002`

### `data/raw/malicious/persistence_persist_download_execute_json/T1197-3_Microsoft-Windows-Sysmon_Operational.json`

- Format: newline-delimited JSON
- Event count: 54
- Common top-level keys: `Event` (54)
- Likely useful fields:
  - `EventID`: present in 54/54 events. Samples: `5`, `1`
  - `Provider`: present in 54/54 events. Samples: `Microsoft-Windows-Sysmon`
  - `Channel`: present in 54/54 events. Samples: `Microsoft-Windows-Sysmon/Operational`
  - `TimeCreated`: present in 54/54 events. Samples: `2024-10-25 17:02:58.8824950`, `2024-10-25 17:02:53.9810327`, `2024-10-25 17:02:53.9872596`
  - `Computer`: present in 54/54 events. Samples: `Server002`
  - `Image`: present in 54/54 events. Samples: `C:\Windows\System32\conhost.exe`, `C:\Windows\System32\HOSTNAME.EXE`, `C:\Windows\System32\whoami.exe`
  - `CommandLine`: present in 25/54 events. Samples: `"C:\Windows\system32\HOSTNAME.EXE"`, `\??\C:\Windows\system32\conhost.exe 0xffffffff -ForceV1`, `"C:\Windows\system32\whoami.exe"`
  - `ParentImage`: present in 20/54 events. Samples: `C:\Windows\System32\HOSTNAME.EXE`, `C:\Windows\System32\whoami.exe`, `C:\Windows\System32\cmd.exe`
  - `User`: present in 54/54 events. Samples: `SERVER002\admin_test`, `NT AUTHORITY\SYSTEM`, `NT AUTHORITY\NETWORK SERVICE`

### `data/raw/malicious/persistence_persist_download_execute_json/T1197-3_Security.json`

- Format: newline-delimited JSON
- Event count: 7
- Common top-level keys: `Event` (7)
- Likely useful fields:
  - `EventID`: present in 7/7 events. Samples: `4616`, `4634`, `4672`
  - `Provider`: present in 7/7 events. Samples: `Microsoft-Windows-Security-Auditing`
  - `Channel`: present in 7/7 events. Samples: `Security`
  - `TimeCreated`: present in 7/7 events. Samples: `2024-10-25 17:02:53.7474748`, `2024-10-25 17:02:53.7503382`, `2024-10-25 17:02:53.9361851`
  - `Computer`: present in 7/7 events. Samples: `Server002`
  - `Image`: present in 2/7 events. Samples: `C:\Windows\System32\svchost.exe`
  - `User`: present in 7/7 events. Samples: `LOCAL SERVICE`, `admin_test`

### `data/raw/malicious/persistence_persist_download_execute_json/T1197-3_System.json`

- Format: newline-delimited JSON
- Event count: 5
- Common top-level keys: `Event` (5)
- Likely useful fields:
  - `EventID`: present in 5/5 events. Samples: `24`, `1`, `35`
  - `Provider`: present in 5/5 events. Samples: `Microsoft-Windows-Kernel-General`, `Microsoft-Windows-Time-Service`
  - `Channel`: present in 5/5 events. Samples: `System`
  - `TimeCreated`: present in 5/5 events. Samples: `2024-10-25 17:02:53.7470517`, `2024-10-25 17:02:53.7472463`, `2024-10-25 17:02:53.7492591`
  - `Computer`: present in 5/5 events. Samples: `Server002`
  - `Image`: present in 2/5 events. Samples: `\Device\HarddiskVolume2\Windows\System32\svchost.exe`

### `data/raw/malicious/persistence_persist_download_execute_json/T1197-3_Windows PowerShell.json`

- Format: empty or whitespace-only
- Event count: 0
- Common top-level keys: none
- Likely useful fields: none extracted
- Note: File is empty or contains only whitespace/BOM content.

